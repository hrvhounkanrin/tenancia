# -*- coding: UTF-8 -*-
"""Immeuble app serializer."""
from rest_framework import serializers

from .models import Immeuble
from proprietaire.models import Proprietaire
from proprietaire.serializers import ProprietaireSerializers


class ImmeubleSerializers(serializers.ModelSerializer):
    """Immeuble serializer."""

    # proprietaire = ProprietaireSerializers(read_only=True)
    proprietaire_id = serializers.PrimaryKeyRelatedField(
        source='Proprietaire',
        queryset=Proprietaire.objects.all(), write_only=True)  # ,

    class Meta:
        """Immeuble serializer meta."""

        model = Immeuble
        fields = ('id', 'intitule', 'description', 'adresse',
                  'jour_emission_facture', 'jour_valeur_facture',
                  'ville', 'quartier', 'pays', 'longitude',
                  'latitude', 'ref_immeuble',
                  'proprietaire_id') #'proprietaire',

    def create(self, validated_data):
        """
        Create Immeuble.

        :rtype: Immeuble
        """
        proprietaire = validated_data.pop('Proprietaire', None)
        return Immeuble.objects.create(proprietaire=proprietaire,
                                       **validated_data)

    def update(self, instance, validated_data):
        """Upddate immeuble."""
        instance.save()
        return instance
