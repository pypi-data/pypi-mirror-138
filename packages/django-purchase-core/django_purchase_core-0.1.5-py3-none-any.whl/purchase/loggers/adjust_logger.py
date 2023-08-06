import time
import logging
import requests

from dataclasses import dataclass
from django.shortcuts import get_object_or_404

from purchase.models import Adjust
from purchase.strings.loggers import ADJUST_URL

logger = logging.getLogger(__name__)


@dataclass
class AdjustLogger:
    fb: dict
    platform: str
    advertiser_id: str
    advertiser_key: str

    @property
    def credentials(self) -> Adjust:
        credentials = get_object_or_404(Adjust, platform=self.platform)
        return credentials

    @property
    def headers(self) -> dict:
        return {"Authorization": f"Bearer {self.credentials.authorization_token}"}

    def log_purchase(self) -> requests.Response:
        response = self.repeatable_request()
        return response

    def get_data(self) -> dict:
        return {
            "revenue": self.fb["value_to_sum"],
            "currency": self.fb["currency"],
            "event_token": self.credentials.purchase_event_token,
            "app_token": self.credentials.app_token,
            "s2s": 1,
            self.advertiser_key: self.advertiser_id,
            "created_at_unix": int(time.time()),
        }

    def repeatable_request(self, trying: int = 3) -> requests.Response:
        while True:
            response = self.request()
            if response.status_code == 200:  # pragma: no cover
                break
            trying -= 1
            if trying <= 0:
                break
            time.sleep(0.1)
        return response

    def request(self) -> requests.Response:
        response = requests.post(
            url=ADJUST_URL, data=self.get_data(), headers=self.headers
        )
        response_text = response.text  # for debugging in sentry  # noqa: F841
        return response
