# -*- coding: UTF-8 -*-
from .models import *
from proprietaire.serializers import ProprietaireSerializers
from proprietaire.models import Proprietaire
from rest_framework import serializers

class ImmeubleSerializers(serializers.ModelSerializer):
    proprietaire = ProprietaireSerializers(read_only=True)
    proprietaire_id = serializers.PrimaryKeyRelatedField(source='Proprietaire',
                                                         queryset=Proprietaire.objects.all(), write_only=True, )
    class Meta:
        model = Immeuble
        fields = ('id', 'intitule', 'description', 'adresse', 'jour_emission_facture',
                  'jour_valeur_facture', 'ville', 'quartier', 'pays', 'longitude',
                  'latitude', 'ref_immeuble', 'proprietaire', 'proprietaire_id')

    def create(self, validated_data):
        proprietaire = validated_data.pop('Proprietaire', None)
        return Immeuble.objects.create(proprietaire=proprietaire, **validated_data)

    def update(self, instance, validated_data):
        instance.save()
        return instance
