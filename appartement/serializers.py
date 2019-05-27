from rest_framework import serializers
from .models import ( ComposantAppartement, Appartement,StructureAppartement, )
#from immeuble.serializers import ImmeubleSerializers
from proprietaire.serializers import ProprietaireSerializers
from immeuble.models import Immeuble
from tools.serializers import RelationModelSerializer
from client.models import Client

class ComposantAppartmentSerializers(serializers.ModelSerializer):
    """ Serializers for model Appartments"""
    class Meta:

        model = ComposantAppartement
        fields = '__all__'

class StructureAppartmentSerializers(serializers.ModelSerializer):

    class Meta:
        model = StructureAppartement
        #fields = ('nbre', 'description',)
        fields = '__all__'



class AppartementSerializers(serializers.ModelSerializer):
    #immeuble = ImmeubleSerializers()
    structures = serializers.SerializerMethodField()
    #structure = StructureAppartmentSerializers(many=True)
    immeuble = serializers.PrimaryKeyRelatedField(queryset=Immeuble.objects.all())
    proprietaire = serializers.SerializerMethodField()
    class Meta:
        model = Appartement
        fields = ('id', 'intitule', 'level', 'autre_description', 'statut', 'immeuble', 'structures', 'proprietaire')


    def get_structures(self, appartement):
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        return StructureAppartmentSerializers(
            structures,
            many=True,
        ).data

    def get_proprietaire(self, appartement):
        id_immeuble=appartement.immeuble.id
        proprietaire = appartement.immeuble.proprietaire
        return ProprietaireSerializers(
            proprietaire,
            many=False,
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
                StructureAppartement(appartement=appartement, composantAppartement=composant_instance,
                                     **structure).save()
        appartement.save()
        return appartement
