from rest_framework import serializers
from .models import *
from client.models import Client

class ComposantAppartmentSerializers(serializers.ModelSerializer):
    """ Serializers for model Appartments"""
    class Meta:
        model = ComposantAppartement
        fields = '__all__'

class AppartementSerializers(serializers.ModelSerializer):

    class Meta:
        model = Appartement
        fields = '__alll__'

class StructureAppartmentSerializers(serializers.ModelSerializer):
    """
    Structure Serializers
    """
    class Meta:
        model = StructureAppartement
        fields = '__all__'


