from rest_framework import serializers
from mcore.serializers import ImmeubleSerializer
from mcore.models import Appartement

class  AppartementSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializer(required=True)

    class Meta:
        model=Appartement
        fields=('intitule', 'nb_sejour', 'nb_chambre', 'nb_salle_a_manger', 
        'nb_cuisine', 'nb_douche', 'autre_description', 'immeuble')