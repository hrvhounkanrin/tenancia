from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from factures.models import  *
# Create your tests here.


class InvoiceOutPut(TestCase):

    def test_call_view_denies_anonymous(self):
        """Get the xml output """

    def test_save_xml_doc(self):
        """ Test to check whether the xml is getting saved and getting output correctly."""
        client = APIClient()
        invoice = Invoice.objects.create()

        inv = InvoiceItem.objects. \
            create(invoice='TestingInvoice')
        url = reverse('invoicing_action/get_invoicing', kwargs={'id': id})

        response = client.get(url)

        self.assertTrue(Invoice.objects.filter(id=id).exists())
