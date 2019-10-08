"""Invoice test case."""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from factures.models import Invoice, InvoiceItem


class InvoiceOutPut(TestCase):
    """Invoice test case."""

    def test_call_view_denies_anonymous(self):
        """Get the xml output."""

    def test_save_xml_doc(self):
        """Test to check whether the xml is getting."""
        client = APIClient()
        Invoice.objects.create()
        InvoiceItem.objects.create(invoice="TestingInvoice")
        url = reverse("invoicing_action/get_invoicing", kwargs={"id": id})
        client.get(url)
        self.assertTrue(Invoice.objects.filter(id=id).exists())
