from rest_framework import serializers , exceptions

from . models import *


class ReglementSerializer(serializers.ModelSerializer):
    """ Reglement serializer"""
    class Meta:
        mode = Reglement
        fields  = '__all__'