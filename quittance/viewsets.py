"""Quitance app viewset."""
from .models import Quittance
from quittance.serializers import QuittanceSerializers
from tools.viewsets import ActionAPIView


class QuittanceActionViewSet(ActionAPIView):
    """Quittance action viewet."""

    def get_quittances(self, request, params={}, *args, **kwargs):
        """Get quitances."""
        get_all_quittances_ = Quittance.objects.all()
        ser_quittance = QuittanceSerializers(
            get_all_quittances_, many=True).data
        return {'success': True, 'quittances': ser_quittance}

    def get_client_per_invoice(self, request, params={}, *args, **kwargs):
        """
        Get client invoice.

        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        get_all_quittances_ = Quittance.objects.all()
        ser_quittance = QuittanceSerializers(
            get_all_quittances_, many=True).data
        return {'success': True, 'quittances': ser_quittance}
