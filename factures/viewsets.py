"""Facture viewsets."""
import logging

from factures.models import Invoice, InvoiceItem, Item
from factures.serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    ItemSerializer,
)
from tools.viewsets import ActionAPIView

LOGGER = logging.getLogger(__name__)
logger = logging.getLogger("ddyxdebug")


class InvoicingActionViewSet(ActionAPIView):
    """Invoicing Action."""

    def get_invoicing(self, request, params={}, *args, **kwargs):
        """
        List service to retrieve  invoicing.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = Invoice.objects.all()
            invoice_serialiazed_data = InvoiceSerializer(queryset, many=True)
            logger.debug(f"**retrieving invoice**" f" --{invoice_serialiazed_data} ")
            logger.info(f"**retrieving invoice** --" f"{invoice_serialiazed_data} ")
            return {"success": True, "response": invoice_serialiazed_data.data}
        except Exception as e:
            return {"success": False, "reason": "%s" % e}

    def get_invoicing_items(self, request, params={}, *args, **kwargs):
        """
        List service to retrieve the invoicing items.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = InvoiceItem.objects.all()
            invoice_item_serialiazed_data = InvoiceItemSerializer(queryset, many=True)
            logger.debug(
                f"**retrieving invoicing items** " f"--{invoice_item_serialiazed_data} "
            )
            logger.info(
                f"**retrieving invoicing items** " f"--{invoice_item_serialiazed_data} "
            )
            return {"success": True, "response": invoice_item_serialiazed_data.data}
        except Exception as e:
            return {"success": False, "reason": "%s" % e}

    def retrieve_items(self, request, params={}, *args, **kwargs):
        """
        List service to retrieve all invoicing items.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = Item.objects.all()
            item_serialiazed_data = ItemSerializer(queryset, many=True)
            logger.debug(f"**retrieving items** --{item_serialiazed_data} ")
            logger.info(f"**retrieving items** --{item_serialiazed_data} ")
            return {"success": True, "response": item_serialiazed_data.data}
        except Exception as e:
            return {"success": False, "reason": "%s" % e}

    def create_invoice(self, request, *args, **kwargs):
        """Set up invoicing."""
        pass
