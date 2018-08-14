from rest_framework import serializers
from mcore.models import Client

class  ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model=Client
        fields=('codebanque', 'libbanque')