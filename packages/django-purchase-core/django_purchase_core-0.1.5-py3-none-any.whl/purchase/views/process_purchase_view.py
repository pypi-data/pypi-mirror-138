import logging

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.generics import CreateAPIView

from purchase.models.choices import PurchaseResponseStatus
from purchase.serializers.request_serialzier import RequestSerialzier
from purchase.serializers.response_serializer import ResponseSerializer
from purchase.controllers.purchase_controller import PurchaseProcessController
from purchase.strings.errors import PURCHASE_ALREADY_CREATE, DATA_IS_NOT_VALID

logger = logging.getLogger(__name__)


class ProcessPurchaseView(CreateAPIView):
    permission_classes = []
    authentication_classes = []
    parser_classes = [JSONParser]
    request_serializer = RequestSerialzier
    response_serializer = ResponseSerializer
    update_player_progress_class = None

    def post(self, request, *args, **kwargs):
        request_data = self.request_serializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        request_data = request_data.validated_data
        response = self.purchase_process(data=request_data)
        return response

    def purchase_process(self, data: dict):
        purchase = PurchaseProcessController(serializer_data=data)

        if purchase.is_create:
            response_data = self.get_response_data(
                status=PurchaseResponseStatus.error, error=PURCHASE_ALREADY_CREATE
            )
            return Response(data=response_data, status=403)

        create_is_done, purchase_model = purchase.try_to_create()
        if not create_is_done:
            response_data = self.get_response_data(
                status=PurchaseResponseStatus.error, error=DATA_IS_NOT_VALID
            )
            return Response(data=response_data, status=403)

        is_sandbox, is_valid = purchase.verify()
        if is_sandbox:
            response_data = self.get_response_data(status=PurchaseResponseStatus.ok)
            return Response(data=response_data, status=201)

        if is_valid:
            purchase.log(purchase_obj=purchase_model)
        else:
            purchase_model.set_transaction_id_to_fake()
        response_data = self.get_response_data(status=PurchaseResponseStatus.ok)
        if self.update_player_progress_class:  # pragma: no cover
            self.update_player_progress()
        return Response(data=response_data, status=201)

    def update_player_progress(self):  # pragma: no cover
        raise NotImplementedError

    def get_response_data(self, status: str, error: str = None):
        serializable_data = {"status": status}
        if error:
            serializable_data.update({"error": error})
        response_data = self.response_serializer(data=serializable_data)
        response_data.is_valid(raise_exception=True)
        return response_data.validated_data
