from rest_framework import serializers , exceptions

from . models import *


class QuittanceSerializers(serializers.ModelSerializer):
    """ Quittance Serializers"""
    class Meta:
        model = Quittance
        fields = '__all__'