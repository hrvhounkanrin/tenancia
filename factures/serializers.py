"""Item serializer."""
import logging

from rest_framework import serializers

from factures.models import Invoice
from factures.models import InvoiceItem
from factures.models import Item

LOGGER = logging.getLogger(__name__)


class ItemSerializer(serializers.ModelSerializer):
    """Item serializer."""

    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        """Get item price."""
        price = obj.price.all().first()
        if price:
            return price.fee

    class Meta:
        """Class Meta defining the model used."""

        model = Item
        read_only_fields = ("id", "item_type")
        exclude = []


class InvoiceItemSerializer(serializers.ModelSerializer):
    """Defining the invoicing serializers."""

    class Meta:
        """Invoice item serializer meta."""

        model = InvoiceItem
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    """Defining Invoicing Serializers."""

    class Meta:
        """Invoice serializer meta."""

        model = Invoice
        fields = "__all__"
