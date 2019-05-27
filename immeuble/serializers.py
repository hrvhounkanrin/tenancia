#from appartement.serializers import (AppartementSerializers,)
from rest_framework import serializers, exceptions
from .models import *
from tools.serializers import RelationModelSerializer
from appartement.models import Appartement
#from appartement.serializers import AppartementSerializers

class ImmeubleSerializers(RelationModelSerializer):
    #appartements = serializers.SerializerMethodField()
    class Meta:
        model = Immeuble
        #fields = '__all__'
        fields = ('id', 'intitule', 'description', 'adresse', 'proprietaire', 'jour_emission_facture',
                  'jour_valeur_facture', 'ville', 'quartier', 'pays', 'longitude', 'latitude', 'ref_immeuble')

    """
    def get_appartements(self, immeuble):
        appartements = Appartement.objects.filter(
            immeuble=immeuble,
        )
        return AppartementSerializers(
            appartements,
            many=True
        ).data
    """

