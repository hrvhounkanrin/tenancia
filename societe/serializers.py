from rest_framework import serializers , exceptions

from . models import *


class SocieteSerializer(serializers.ModelSerializer):
    """ Reglement serializer"""
    class Meta:
        mode = Societe
        fields  = '__all__'