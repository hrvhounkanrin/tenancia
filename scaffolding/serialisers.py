# -*- coding: UTF-8 -*-
"""Scaffolding serializer."""
from django.db import transaction
from rest_framework import serializers

from .models import Appartement
from .models import Immeuble
from .models import StructureAppartement
from appartement.models import ComposantAppartement
from appartement.serializers import ComposantAppartmentSerializers


class ImmeubleSerializers(serializers.ModelSerializer):
    """Immeuble serializer."""

    class Meta:
        """Immeuble serializer meta."""

        model = Immeuble
        fields = '__all__'


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """StructureApparement serializer."""

    composantAppartement = ComposantAppartmentSerializers(read_only=True)
    composantAppartement_id = serializers.PrimaryKeyRelatedField(
        source='ComposantAppartement',
        queryset=ComposantAppartement.objects.all(), write_only=True,)

    class Meta:
        """Structure appatement serializer meta."""

        model = StructureAppartement
        fields = ['appartement', 'composantAppartement',
                  'composantAppartement_id', 'nbre',
                  'description', 'is_periodic']


class AppartementSerializers(serializers.ModelSerializer):
    """Appartement serializer."""

    structures = serializers.SerializerMethodField()
    immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source='Immeuble', queryset=Immeuble.objects.all(), write_only=True, )

    class Meta:
        """Apapartement serializer meta."""

        model = Appartement
        fields = ('id', 'intitule', 'level', 'autre_description',
                  'statut', 'immeuble', 'immeuble_id', 'structures',)

    def get_structures(self, appartement):
        """Get appartment structure."""
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        return StructureAppartmentSerializers(
            structures,
            many=True,
        ).data

    @transaction.atomic
    def create(self, validated_data):
        """
        Create appartement.

        :rtype: Immeuble
        """
        immeuble = validated_data.pop('Immeuble', None)
        appartement_instance = Appartement.objects.create(
            immeuble=immeuble, **validated_data)
        if 'structures' in self.initial_data:
            structures = self.initial_data.get('structures')
            for structure in structures:
                StructureAppartement(appartement=appartement_instance,
                                     **structure).save()
            appartement_instance.save()
        return appartement_instance

    # TODO : Changer le update pour le rendre plus agnostique des attributs
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update appartement."""
        instance.intitule = validated_data['intitule']
        instance.level = validated_data['level']
        instance.autre_description = validated_data['autre_description']
        instance.statut = validated_data['statut']
        instance.save()
        if 'structures' in self.initial_data:
            StructureAppartement.objects.filter(
                appartement__id=instance.id).delete()
            structures = self.initial_data.get('structures')
            for structure in structures:
                StructureAppartement(appartement=instance, **structure).save()
        return instance
