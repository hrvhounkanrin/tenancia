from rest_framework import serializers
from mcore.serializers import ContratSerializer
from mcore.models import (Quittance, )

class  QuittanceSerializer(serializers.ModelSerializer):
    contrat = ContratSerializer(required=True)

    class Meta:
        model=Quittance
        fields=(
            'reference',
            'date_emission',
            'date_valeur', 
            'debut_periode', 
            'fin_periode', 
            'nature', 
            'montant', 
            'statut', 
            'date_statut', 
            'contrat',
            'motif_annulation')