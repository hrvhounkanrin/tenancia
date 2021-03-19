# -*- coding: UTF-8 -*-
"""Housing app serializers."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from django.utils.crypto import get_random_string
from .models import Appartement
from .models import ComposantAppartement
from .models import StructureAppartement
from immeuble.models import Immeuble
from immeuble.serializers import ImmeubleSerializers


class ComposantAppartmentSerializers(serializers.ModelSerializer):
    """ComposantApapartement(Housing dependecy type) serializer."""

    class Meta:
        """ComposantApapartement serializer meta."""

        model = ComposantAppartement
        fields = '__all__'


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """Housing dependecies of specfic housing."""

    composantAppartement =\
        ComposantAppartmentSerializers(read_only=True)
    composantAppartement_id = serializers.PrimaryKeyRelatedField(
        source='ComposantAppartement',
        queryset=ComposantAppartement.objects.all(),
        write_only=True, )

    class Meta:
        """StructureAppartement meta."""

        model = StructureAppartement
        fields = ['appartement', 'composantAppartement',
                  'composantAppartement_id', 'nbre',
                  'description', 'is_periodic']


class AppartementSerializers(serializers.ModelSerializer):
    """Housing serializer."""

    structures = serializers.SerializerMethodField()
    # immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source='Immeuble', queryset=Immeuble.objects.all(), write_only=True, )

    class Meta:
        """Housing serializer meta."""

        model = Appartement
        fields = ('id', 'intitule', 'level', 'autre_description', 'statut', 'immeuble_id', 'structures',) # 'immeuble',

    def get_structures(self, appartement):
        """Get housing dependecies.

        :param appartement:
        :return:
        """
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        return StructureAppartmentSerializers(
            structures,
            many=True,
        ).data

    @transaction.atomic
    def create(self, validated_data):
        """Create housing.

        :rtype: Appartement
        """
        immeuble = validated_data.pop('Immeuble', None)
        logement_instance = Appartement.objects.create(
            immeuble=immeuble, **validated_data)
        if 'structures' in self.initial_data:
            structures = self.initial_data.get('structures')
            for structure in structures:
                dependency_id = structure.pop('composantAppartement', None)
                try:
                    dependency_instance = \
                        ComposantAppartement.objects.get(id=dependency_id)
                except ObjectDoesNotExist:
                    continue
                structure.pop("appartement", None)
                print(structure)
                StructureAppartement(appartement=logement_instance,
                                     composantAppartement=dependency_instance,
                                     **structure).save()
            logement_instance.save()
        return logement_instance

    # TODO : Check whether Component exist before saving structure
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update housing."""
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
                structure.pop("appartement", None)
                print(structure)
                # StructureAppartement(appartement=instance, **structure).save()
        return instance


class MultiplyAppartementSerializer(serializers.Serializer):
    nb = serializers.IntegerField(default=1)
    appartement_id = serializers.IntegerField()

    @transaction.atomic
    def create(self, validated_data):

        try:
            appartement = Appartement.objects.get(validated_data['appartement_id'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError("L'appartement que vous voulez reproduire n'existe pas.")

        user = self.context['request'].user
        appartements = []
        appartement = Appartement.objects.get(pk=validated_data['appartement_id'])
        appartement_fields = list(appartement.__dict__.keys())
        appartement_fields = [f for f in appartement_fields if f not in ['id', 'created_by_id', 'modified_by_id', '_state']]
        for i in range(validated_data['nb']):
            new_appartement = Appartement()
            for field in list(appartement_fields):

                field_name_val = getattr(appartement, field)
                # print(f'field_value: {field_name_val}')
                setattr(new_appartement, field, field_name_val)
            appartements.append(new_appartement)
        [m.save(intitule=get_random_string(8).upper(), created_by_id=user.id) for m in appartements]
        return {'nb': validated_data['nb'], 'appartement_id': validated_data['appartement_id']}
