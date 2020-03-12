"""Facture managements."""
from django.core.management.base import BaseCommand
from tools import send_invoices


class Command(BaseCommand):
    """Send invoice command."""

    help = "Send due invoices"

    def handle(self, *args, **options):
        """Handle send invoice command."""
        send_invoices()
