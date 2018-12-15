from rest_framework import serializers
from mcore.serializers import ContratSerializer
from mcore.models import (Facture, )

class  FactureSerializer(serializers.ModelSerializer):
    contrat = ContratSerializer(required=True)

    class Meta:
        model=Facture
        fields=('reference', 'date_emission', 'date_valeur', 'debut_periode', 
                'fin_periode', 'nature', 'montant', 'statut', 'date_statut', 
                'contrat',)