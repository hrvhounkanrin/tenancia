from rest_framework import serializers , exceptions

from .models import *
#pip install xmtodict later on /'''


class ContratSerializers(serializers.ModelSerializer):
    class Meta:
        model = Contrat
        fields =('id', 'reference_bail', 'date_signature', 'date_effet', 'periodicite', 'periodicite', 'duree',
                 'montant_bail', 'statut', 'caution_loyer', 'caution_eau' , 'caution_electricite', 'observation',
                 'tacite_reconduction', 'client', 'appartement')