from rest_framework import serializers, exceptions
from proprietaire.serializers import ProprietaireSerializers
from proprietaire.models import  Proprietaire
from .models import *
from tools.serializers import AsymetricRelatedField


class ImmeubleSerializers(serializers.ModelSerializer):
    """ Immeuble Seriaizers"""
    #proprietaire = ProprietaireSerializers()
    #proprietaire = AsymetricRelatedField.from_serializer(ProprietaireSerializers)
    class Meta:
        model = Immeuble
        fields = '__all__'