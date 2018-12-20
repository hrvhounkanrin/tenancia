from rest_framework import serializers , exceptions

from .models import *

class ImmeubleSerializers(serializers.ModelSerializer):
    """ Immeuble Seriaizers"""
    class Meta:
        model = Immeuble
        fields = '__all__'
