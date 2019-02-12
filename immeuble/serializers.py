from rest_framework import serializers, exceptions
from proprietaire.serializers import ProprietaireSerializers
from .models import *


class ImmeubleSerializers(serializers.ModelSerializer):
    """ Immeuble Seriaizers"""
    proprietaire = ProprietaireSerializers()

    class Meta:
        model = Immeuble
        fields = '__all__'
