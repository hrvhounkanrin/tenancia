from rest_framework import serializers
from .models import (StructureAppartement, ComposantAppartement, Appartement, )
#from immeuble.serializers import ImmeubleSerializers
from tools.serializers import RelationModelSerializer
from client.models import Client

class ComposantAppartmentSerializers(RelationModelSerializer):
    """ Serializers for model Appartments"""
    class Meta:
        model = ComposantAppartement
        fields = '__all__'


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """
    Structure Serializers
    """
    composantAppartement = ComposantAppartmentSerializers(read_only=False, is_relation=True)
    #appartement = AppartementSerializers(read_only=False, is_relation=True)

    class Meta:
        model = StructureAppartement
        fields = ('appartement', "composantAppartement", 'nbre', 'description', )


class AppartementSerializers(RelationModelSerializer):
    #immeuble = ImmeubleSerializers(read_only=False, is_relation=True)
    structures = serializers.SerializerMethodField()
    #structure = StructureAppartmentSerializers(many=True)
    class Meta:
        model = Appartement
        fields = ('id', 'intitule', 'level', 'autre_description', 'statut', 'immeuble', 'structures' )


    def get_structures(self, appartement):
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        return StructureAppartmentSerializers(
            structures,
            many=True,
        ).data

    def create(self, validated_data):
        structures_data = self.initial_data['structures']
        print(structures_data)
        appartement = Appartement.objects.create(**validated_data)
        if "structures" in self.initial_data:
            structures = self.initial_data.get("structures")
            for structure in structures:
                composant_id = structure.get("composantAppartement", None)
                composant_instance = ComposantAppartement.objects.get(pk=composant_id)
                structure.pop('composantAppartement')
                structure.pop('appartement')
                StructureAppartement(appartement=appartement, composantAppartement=composant_instance, **structure).save()
        appartement.save()
        return appartement

