from rest_framework import serializers
from msecurity.serializers import UserSerializer
from mcore.models import Client

class  ClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    class Meta:
        model=Client
        fields=('user', 'ice', 'ice_number', 'ice_relation')