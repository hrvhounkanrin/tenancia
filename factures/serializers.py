import logging

from rest_framework import serializers

from factures.models import *

LOGGER = logging.getLogger(__name__)


class ItemSerializer(serializers.ModelSerializer):
    """ So far so good with the  serializer class of the items -serialize the model Item"""
    price = serializers.SerializerMethodField()

    def get_price(self, obj):
        price = obj.price.all().first()
        if price:
            return price.fee

    class Meta:
        """Class Meta defining the model used and  placed an option on the read_only_fields"""
        model = Item
        read_only_fields = ('id', 'item_type')
        exclude = []


class InvoiceItemSerializer(serializers.ModelSerializer):
    """ Defining the invoicing serializers"""

    class Meta:
        model = InvoiceItem
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    """ Defining Invoicing Serializers"""
    class Meta:
        model = Invoice
        fields = '__all__'
