from rest_framework import serializers
from mcore.models import Banque

class  BanqueSerializer(serializers.ModelSerializer):
    class Meta:
        model=Banque
        fields=('codebanque', 'libbanque')