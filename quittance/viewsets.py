"""Quitance app viewset."""
import datetime
import logging

from contrat.models import Contrat, ContratAccessoiresloyer
from quittance.serializers import  QuittanceSerializers
from tools.viewsets import ActionAPIView

from .models import Quittance

logger = logging.getLogger(__name__)

FILTER_PARAMS = {
    'id': 'id',
    'contrat': 'contrat_id',
    'client': 'client_id',
    'color': 'values__something__color__name__iexact'
}




class QuittanceActionViewSet(ActionAPIView):
    """Quittance action viewet."""

    def _get_filter_params(self, query_params):
        fields = {}

        for k, v in query_params.items():
            if k in self.FILTER_PARAMS:
                fields[self.FILTER_PARAMS[k]] = v
        return fields

    def get_tenant_quittances(self, request, params={}, *args, **kwargs):
        """Get quitances."""
        # filter_params = self.get_filter_params(self.request.query_params)
        queryset = Quittance.objects.filter(tenant_user_id=request.user.id)
        if "id" in params:
            queryset = Quittance.objects.filter(id__in=params["id"].split(","), tenant_user_id=request.user.id)
        if "contrat_id" in params:
            queryset = Quittance.objects.filter(
                contrat_id__in=params["contrat_id"].split(","), tenant_user_id=request.user.id
            )
        serializer = QuittanceSerializers(
            queryset, context={"request": request}, many=True
        )
        logger.debug("**retrieving Quittance **")
        return {"success": True, "payload": serializer.data}

    def get_lessor_quittances(self, request, params={}, *args, **kwargs):
        """Get quitances."""
        # filter_params = self.get_filter_params(self.request.query_params)
        queryset = Quittance.objects.filter(lessor_user_id=request.user.id)
        if "id" in params:
            queryset = Quittance.objects.filter(id__in=params["id"].split(","), lessor_user_id=request.user.id)
        if "contrat_id" in params:
            queryset = Quittance.objects.filter(
                contrat_id__in=params["contrat_id"].split(","), lessor_user_id=request.user.id
            )
        serializer = QuittanceSerializers(
            queryset, context={"request": request}, many=True
        )
        logger.debug("**retrieving Quittance **")
        return {"success": True, "payload": serializer.data}

    def get_client_per_invoice(self, request, params={}, *args, **kwargs):
        """
        Get client invoice.

        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        get_all_quittances_ = Quittance.objects.all()
        ser_quittance = QuittanceSerializers(get_all_quittances_, many=True).data
        return {"success": True, "quittances": ser_quittance}
