"""Quitance app viewset."""
import datetime
import logging

from contrat.models import Contrat, ContratAccessoiresloyer
from quittance.serializers import FirstQuittanceSerializers, QuittanceSerializers
from tools.viewsets import ActionAPIView

from .models import Quittance

logger = logging.getLogger(__name__)


class QuittanceActionViewSet(ActionAPIView):
    """Quittance action viewet."""

    def get_quittances(self, request, params={}, *args, **kwargs):
        """Get quitances."""

        if "id" in params:
            queryset = Quittance.objects.filter(id__in=params["id"].split(","))
        if "contrat_id" in params:
            queryset = Quittance.objects.filter(
                contrat_id__in=params["contrat_id"].split(",")
            )
        serializer = QuittanceSerializers(
            queryset, context={"request": request}, many=True
        )
        logger.debug("**retrieving Quittance **")
        return {"success": True, "quittances": serializer.data}

    def create_first_quittance(self, request, params={}, *args, **kwargs):
        """Create contract."""
        serializer_context = {
            "request": request,
        }
        print(f"params: {params}")
        serializer = FirstQuittanceSerializers(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "quittances": serializer.data}

    def create_first_quittance(self, request, params={}, *args, **kwargs):
        """Create contract."""
        serializer_context = {
            "request": request,
        }
        print(f"params: {params}")
        serializer = FirstQuittanceSerializers(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "quittances": serializer.data}

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
