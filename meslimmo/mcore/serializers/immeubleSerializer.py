from rest_framework import serializers
from mcore.serializers import ProprietaireSerializer
from mcore.serializers import CountrySerializer
from mcore.models import Proprietaire

class  ImmeubleSerializer(serializers.ModelSerializer):
    proprietaire = ProprietaireSerializer(required=True)
    pays = CountrySerializer(required=False)
    class Meta:
        model=Proprietaire
        fields=(
            'intitule',
            'description', 
            'adresse', 
            'proprietaire', 
            'jour_emission_facture',
            'jour_valeur_facture',
            'ville',
            'quartier', 
            'ref_immeuble',
            'pays',
            'longitude',
            'latitude')