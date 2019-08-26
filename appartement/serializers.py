# -*- coding: UTF-8 -*-
from django.db import transaction
from rest_framework import serializers
from .models import ( ComposantAppartement, Appartement,StructureAppartement, )
from proprietaire.serializers import ProprietaireSerializers
from immeuble.models import Immeuble
from immeuble.serializers import ImmeubleSerializers

class ComposantAppartmentSerializers(serializers.ModelSerializer):
    """ Serializers for model Appartments"""
    class Meta:

        model = ComposantAppartement
        fields = '__all__'

class StructureAppartmentSerializers(serializers.ModelSerializer):
    composantAppartement = ComposantAppartmentSerializers(read_only=True)
    composantAppartement_id = serializers.PrimaryKeyRelatedField(source='ComposantAppartement', queryset=ComposantAppartement.objects.all(), write_only=True, )
    class Meta:
        model = StructureAppartement
        fields = ['appartement', 'composantAppartement', 'composantAppartement_id', 'nbre',
                  'description', 'is_periodic']



class AppartementSerializers(serializers.ModelSerializer):
    structures = serializers.SerializerMethodField()
    immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(source='Immeuble', queryset=Immeuble.objects.all(), write_only=True, )

    class Meta:
        model = Appartement
        fields = ('id', 'intitule', 'level', 'autre_description', 'statut', 'immeuble', 'immeuble_id', 'structures',)


    def get_structures(self, appartement):
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        return StructureAppartmentSerializers(
            structures,
            many=True,
        ).data


    @transaction.atomic
    def create(self, validated_data):
        immeuble = validated_data.pop('Immeuble', None)
        logement_instance = Appartement.objects.create(immeuble=immeuble, **validated_data)
        if "structures" in self.initial_data:
            structures = self.initial_data.get("structures")
            for structure in structures:
                structure.pop('appartement', None)
                StructureAppartement(appartement=logement_instance, **structure).save()
            logement_instance.save()
        return logement_instance

    # TODO : Check whether Component exist before saving structure
    @transaction.atomic
    def update(self, instance, validated_data):
        print(instance)
        instance.intitule = validated_data['intitule']
        instance.level = validated_data['level']
        instance.autre_description = validated_data['autre_description']
        instance.statut = validated_data['statut']
        #instance.statut = validated_data['statut']
        instance.save()
        if "structures" in self.initial_data:
            StructureAppartement.objects.filter(appartement__id=instance.id).delete()
            structures = self.initial_data.get("structures")
            for structure in structures:
                StructureAppartement(appartement=instance,**structure).save()
        return instance

