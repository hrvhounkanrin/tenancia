from rest_framework import serializers
from mcore.serializers import AppartementSerializer
from mcore.serializers import ComposantAppartementSerializer
from mcore.models import Appartement
from mcore.models import ComposantAppartement
from mcore.models import StructureAppartement

class  StructureAppartementSerializer(serializers.ModelSerializer):
    appartement = AppartementSerializer(required=True)
    composant = ComposantAppartementSerializer(required=True)

    class Meta:
        model=StructureAppartement
        fields=(
            'appartement',
            'composant', 
            'nbre', 
            'description'
            )