from rest_framework import serializers
from msecurity.serializers import UserSerializer
from mcore.serializers import BanqueSerializer
from mcore.serializers import CountrySerializer
from mcore.models import Proprietaire

class  ProprietaireSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    banque = BanqueSerializer(required=False)
    pays_residence = CountrySerializer(required=False)
    class Meta:
        model=Proprietaire
        fields=('user', 'mode_paiement', 'numcompte', 'banque','pays_residence')