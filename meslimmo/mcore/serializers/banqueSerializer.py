from rest_framework import serializers
from mcore.models import Banque
from mcore.serializers import CountrySerializer
class  BanqueSerializer(serializers.ModelSerializer):
    pays = CountrySerializer(required=False)
    class Meta:
        model=Banque
        fields=('codebanque', 'libbanque')