from rest_framework import serializers
from mcore.serializers import ImmeubleSerializer
from mcore.models import Appartement

class  AppartementSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializer(required=True)

    class Meta:
        model=Appartement
        fields=(
            'intitule',
            'level', 
            'autre_description', 
            'immeuble'
            'structure',
            'statut')