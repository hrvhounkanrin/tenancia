from factures.models import *
import logging
from rest_framework.serializers import Serializer
from tools.viewsets import ActionAPIView
from factures.serializers import *

LOGGER = logging.getLogger(__name__)
logger = logging.getLogger('ddyxdebug')


class InvoicingAction(ActionAPIView):
    """ Invoicing Action"""

    def get_invoicing(self, request, params={}, *args, **kwargs):
        """
         Listing service to retrieve  invoicing
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = Invoice.objects.all()
            invoice_serialiazed_data = InvoiceSerializer(queryset, many=True, )
            logger.debug(f'**retrieving invoice** --{invoice_serialiazed_data} ')
            logger.info(f'**retrieving invoice** --{invoice_serialiazed_data} ')
            return {'success': True, 'response': invoice_serialiazed_data.data}
        except Exception as e:
            return {'success': False, 'reason': '%s' % e}

    def get_invoicing_items(self, request, params={}, *args, **kwargs):
        """
         Listing service to retrieve the invoicing items
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = InvoiceItemSerializer.objects.all()
            invoice_item_serialiazed_data = InvoiceSerializer(queryset, many=True, )
            logger.debug(f'**retrieving invoicing items** --{invoice_item_serialiazed_data} ')
            logger.info(f'**retrieving invoicing items** --{invoice_item_serialiazed_data} ')
            return {'success': True, 'response': invoice_item_serialiazed_data.data}
        except Exception as e:
            return {'success': False, 'reason': '%s' % e}

    def retrieve_items(self, request, params={}, *args, **kwargs):
        """
         Listing service to retrieve all invoicing items.
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        try:
            queryset = ItemSerializer.objects.all()
            item_serialiazed_data = InvoiceSerializer(queryset, many=True, )
            logger.debug(f'**retrieving items** --{item_serialiazed_data} ')
            logger.info(f'**retrieving items** --{item_serialiazed_data} ')
            return {'success': True, 'response': item_serialiazed_data.data}
        except Exception as e:
            return {'success': False, 'reason': '%s' % e}



