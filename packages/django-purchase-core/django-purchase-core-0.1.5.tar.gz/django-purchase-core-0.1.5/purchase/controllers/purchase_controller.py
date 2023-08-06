import json
import logging

from django.db import transaction

from purchase.models.choices import Platform
from purchase.strings.loggers import ADJUST_URL
from purchase.verifiers.apple_verifier import AppleVerifier
from purchase.verifiers.google_verifier import GoogleVerifier
from purchase.loggers.adjust_logger import AdjustLogger
from purchase.loggers.facebook_logger import FacebookLogger
from purchase.models import Purchase, Log, AdjustLog, Config
from purchase.loggers.apps_flyer_logger import AppsFlyerLogger
from purchase.strings.errors import (
    APPSFLYER_ID_NOT_FOUND,
    ALL_ZEROS,
    ADJUST_ADVERTISER_NOT_FOUND,
)
from purchase.strings.log_levels import (
    PURCHASE_CREATE,
    GOOGLE_ERROR_LEVEL,
    APPLE_ERROR_LEVEL,
    FACEBOOK_LOGGING_ERROR_LEVEL,
    ADJUST_ERROR_LEVEL,
    APPS_FLYER_ERROR_LEVEL,
)

logger = logging.getLogger(__name__)


class PurchaseProcessController:
    def __init__(self, serializer_data: dict):
        self.serializer_data = serializer_data
        self.platform = serializer_data["platform"]
        self.fb = serializer_data["data"]["fb"]
        self.version = self.fb["bundle_short_version"]
        self.is_sandbox = serializer_data["is_sandbox"]
        self.receipt_data = serializer_data["data"]["receipt_data"]

    @property
    def appsflyer_id(self):
        if (
            "appsflyer_id" not in self.serializer_data["data"]
            or self.serializer_data["data"]["appsflyer_id"] is None
        ):  # pragma: no cover
            raise ValueError(APPSFLYER_ID_NOT_FOUND)
        return self.serializer_data["data"]["appsflyer_id"]

    @property
    def transaction_id(self):
        if self.platform == Platform.android:
            return self.get_transaction_id_from_json()
        else:
            return self.serializer_data["data"]["receipt_data"]["transaction_id"]

    def get_details_for_log(self):
        return {"transaction_id": self.transaction_id, "data": self.serializer_data}

    def get_advertiser_id(self):  # pragma: no cover
        advertiser_id = self.fb["advertiser_id"]
        if advertiser_id is None or advertiser_id == ALL_ZEROS or advertiser_id == "":
            if "adjust_device_id" not in self.serializer_data["data"]:
                raise ValueError(ADJUST_ADVERTISER_NOT_FOUND)
            return "adid", self.serializer_data["data"]["adjust_device_id"]
        if self.platform == Platform.android:
            return "gps_adid", advertiser_id
        if self.platform == Platform.ios:
            return "idfa", advertiser_id

    def get_transaction_id_from_json(self):
        try:
            payload = json.loads(self.receipt_data["payload"])
            payload_json = json.loads(payload["json"])
            return payload_json["orderId"]
        except Exception as err:  # pragma: no cover
            logger.error(
                f"JSON parsing of transaction_id from payload on Android: {err}"
            )

    @property
    def is_create(self):
        return Purchase.objects.filter(
            transaction_id=self.transaction_id, platform=self.platform
        ).exists()

    @transaction.atomic
    def create(self):
        args = {
            "transaction_id": self.transaction_id,
            "advertiser_id": self.fb["advertiser_id"],
            "platform": self.platform,
            "fb_user_id": self.fb["user_id"],
            "bundle_short_version": self.fb["bundle_short_version"],
            "ext_info": self.fb["extinfo"],
            "product_id": self.fb["product_id"],
            "value_to_sum": self.fb["value_to_sum"],
            "log_time": self.fb["log_time"],
            "currency": self.fb["currency"],
            "is_sandbox": self.is_sandbox,
            "body": self.serializer_data,
        }
        return Purchase.objects.create(**args)

    @transaction.atomic
    def save_error_log(self, error_message: str, log_level: str, details: dict):
        Log.objects.create(
            platform=self.platform,
            version=self.version,
            log_level=log_level,
            message=error_message,
            details=details,
        )

    def try_to_create(self) -> (bool, Purchase or bool):
        try:
            purchase_obj = self.create()
            return True, purchase_obj
        except Exception as err:
            self.save_error_log(
                error_message=str(err),
                log_level=PURCHASE_CREATE,
                details=self.serializer_data,
            )
            return False, False

    def verify(self) -> (bool, bool):
        if self.platform == Platform.android:
            return self.google_verify()
        if self.platform == Platform.ios:
            return self.apple_verify()

    def apple_verify(self) -> (bool, bool):
        is_sandbox = self.is_sandbox
        result = False
        try:
            apple_verifier = AppleVerifier(
                receipt=self.receipt_data,
                is_sandbox=self.is_sandbox,
                product_id=self.serializer_data["data"]["fb"]["product_id"],
                platform=self.platform,
                version=self.version,
                transaction_id=self.transaction_id,
            )
            is_sandbox, result = apple_verifier.verify()
        except Exception as err:  # pragma: no cover
            details = {
                "transaction_id": self.transaction_id,
                "receipt": self.receipt_data,
            }
            self.save_error_log(
                error_message=str(err), log_level=APPLE_ERROR_LEVEL, details=details
            )
        return is_sandbox, result

    def google_verify(self) -> (bool, bool):
        result = False
        try:
            google_verifier = GoogleVerifier(
                receipt=self.receipt_data,
                platform=self.platform,
                version=self.version,
            )
            result = google_verifier.verify_purchase()
        except Exception as err:  # pragma: no cover
            details = {
                "transaction_id": self.transaction_id,
                "receipt": self.receipt_data,
            }
            self.save_error_log(
                error_message=str(err), log_level=GOOGLE_ERROR_LEVEL, details=details
            )
        return self.is_sandbox, result

    def log_in_facebook(self, purchase_obj: Purchase):
        fb_logger = FacebookLogger(
            platform=self.platform,
            transaction_id=self.transaction_id,
            fb_data=self.fb,
        )
        response = fb_logger.log_purchase()
        if response.status_code != 200:
            err = f"api error: request error [{response.url}] {response.status_code = }, {response.text = }"
            self.save_error_log(
                error_message=err,
                log_level=FACEBOOK_LOGGING_ERROR_LEVEL,
                details=self.get_details_for_log(),
            )
        else:  # pragma: no cover
            purchase_obj.fb_is_logged = True
            purchase_obj.save()

    def log_in_appsflyer(self, purchase_obj: Purchase):
        appsflyer_logger = AppsFlyerLogger(
            platform=self.platform,
            appsflyer_id=self.appsflyer_id,
            fb=self.fb,
        )
        response = appsflyer_logger.log_purchase()
        if response.status_code != 200:
            err = f"api error: request error [{response.url}] {response.status_code = }, {response.text = }"
            self.save_error_log(
                error_message=err,
                log_level=APPS_FLYER_ERROR_LEVEL,
                details=self.get_details_for_log(),
            )
        else:  # pragma: no cover
            purchase_obj.af_is_logged = True
            purchase_obj.save()

    def log_in_adjust(self, purchase_obj: Purchase):
        advertiser_key, advertiser_id = self.get_advertiser_id()
        adjust_logger = AdjustLogger(
            fb=self.fb,
            platform=self.platform,
            advertiser_id=advertiser_id,
            advertiser_key=advertiser_key,
        )
        response = adjust_logger.log_purchase()
        AdjustLog.objects.get_or_create(
            purchase=purchase_obj,
            request_url=ADJUST_URL,
            response=response.text,
            request_data=adjust_logger.get_data(),
            request_headers=adjust_logger.headers,
        )
        if response.status_code != 200:
            error_details = f"api error: request error [{response.url}] {response.status_code = }, {response.text = }"
            logger.exception(error_details)
            self.save_error_log(
                log_level=ADJUST_ERROR_LEVEL,
                error_message=error_details,
                details=self.get_details_for_log(),
            )

    def get_enable_loggers(self):
        loggers = {
            self.log_in_adjust: True,
            self.log_in_appsflyer: True,
            self.log_in_facebook: True,
        }
        associated_config = Config.objects.filter(
            platform=self.platform
        )
        if associated_config.exists():
            config = associated_config.first()
            loggers = {
                self.log_in_adjust: config.is_adjust_log_enabled,
                self.log_in_appsflyer: config.is_af_log_enabled,
                self.log_in_facebook: config.is_fb_log_enabled,
            }
        return loggers

    def log(self, purchase_obj: Purchase):
        enabled_loggers = self.get_enable_loggers()
        if enabled_loggers[self.log_in_adjust]:
            self.log_in_adjust(purchase_obj=purchase_obj)
        if enabled_loggers[self.log_in_facebook]:
            self.log_in_facebook(purchase_obj=purchase_obj)
        if enabled_loggers[self.log_in_appsflyer]:
            self.log_in_appsflyer(purchase_obj=purchase_obj)
