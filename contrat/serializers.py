from rest_framework import serializers
from .models import (Accesoireloyer, Contrat, ContratAccessoiresloyer, )
from appartement.models import (Appartement, )
#from immeuble.serializers import ImmeubleSerializers
from tools.serializers import RelationModelSerializer
from client.models import Client

from .models import *
#pip install xmtodict later on /'''

class AccesoireloyerSerializers(RelationModelSerializer):
    """ Serializers for model Accesoireloyer"""
    class Meta:
        model = Accesoireloyer
        fields = '__all__'

class ContratAccessoiresloyerSerializers(serializers.ModelSerializer):
    """
    Structure Serializers
    """
    accesoireloyer = AccesoireloyerSerializers(read_only=False, is_relation=True)
    #appartement = AppartementSerializers(read_only=False, is_relation=True)

    class Meta:
        model = ContratAccessoiresloyer
        fields = ('contrat', "accesoireloyer", 'montant', 'devise', 'statut', 'devise', 'description')

class ContratSerializers(serializers.ModelSerializer):
    accessoires = serializers.SerializerMethodField()
    class Meta:
        model = Contrat
        fields =('id', 'reference_bail', 'date_signature', 'date_effet', 'periodicite', 'duree',
                 'montant_bail', 'statut', 'observation', 'tacite_reconduction',
                 'client', 'appartement', 'accessoires')

    def get_accessoires(self, contrat):
        accessoires = ContratAccessoiresloyer.objects.filter(
            contrat=contrat.id,
        )
        return ContratAccessoiresloyerSerializers(
            accessoires,
            many=True,
        ).data

    def create(self, validated_data):
        contrat = Contrat.objects.create(**validated_data)
        if "accessoires" in self.initial_data:
            accessoires = self.initial_data.get("accessoires")
            for accessoire in accessoires:
                accessoire_id = accessoire.get("accessoire", None)
                accessoire_instance = Accesoireloyer.objects.get(pk=accessoire_id)
                accessoire_id = accessoire.pop('accessoire')
                print(accessoire)
                ContratAccessoiresloyer(contrat=contrat, accesoireloyer=accessoire_instance, **accessoire).save()
        #contrat.save()
        return contrat