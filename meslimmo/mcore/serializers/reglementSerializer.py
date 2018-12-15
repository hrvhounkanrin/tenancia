from rest_framework import serializers
from mcore.serializers import FactureSerializer
from mcore.models import (Reglement, )

class  ReglementSerializer(serializers.ModelSerializer):
    facture = FactureSerializer(required=True)

    class Meta:
        model=Reglement
        fields=('reference', 'date_reglement', 'date_valeur', 'montant', 
                'statut', 'date_statut', 'regle_par', 'num_telephone', 'mode_reglement', 
                'reference_transaction','facture')