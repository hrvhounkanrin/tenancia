from rest_framework import serializers
from mcore.serializers import AppartementSerializer
from mcore.models import (Contrat, )

class  ContratSerializer(serializers.ModelSerializer):
    appartement = AppartementSerializer(required=True)

    class Meta:
        model=Contrat
        fields=('reference_bail', 'date_signature', 'date_effet', 'duree', 
                'periodicite', 'montant_bail', 'statut', 'caution_loyer', 'caution_eau', 
                'caution_electricite', 'observation', 'client', 'appartement')