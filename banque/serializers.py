from rest_framework import serializers
from .models import *

class BanqueSerializers(serializers.ModelSerializer):
    """ Banque Model serializer"""

    class Meta:
        model = Banque
        fields = '__all__'
        extra_kwargs = {
            'codebanque': {'validators': []},
        }