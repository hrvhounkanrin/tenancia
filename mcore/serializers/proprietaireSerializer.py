from rest_framework import serializers
from msecurity.serializers import UserSerializer
from mcore.serializers import BanqueSerializer
from mcore.models import Proprietaire

class  ProprietaireSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    banque = BanqueSerializer(required=False)
    class Meta:
        model=Proprietaire
        fields=('user', 'mode_paiement', 'numcompte', 'banque')