"""Appartment Serializers."""
import logging

from rest_framework import serializers

from .models import Appartement
from .models import ComposantAppartement
from .models import StructureAppartement
from tools.serializers import RelationModelSerializer

LOGGER = logging.getLogger(__name__)
logger = logging.getLogger('ddyxdebug')


class ComposantAppartmentSerializers(RelationModelSerializer):
    """Serializers for model Appartments."""

    class Meta:
        """Meta."""

        model = ComposantAppartement
        fields = '__all__'


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """Structure Serializers."""

    composantAppartement = \
        ComposantAppartmentSerializers(read_only=False,
                                       is_relation=True)

    class Meta:
        """Meta."""

        model = StructureAppartement
        fields = ('appartement',
                  'composantAppartement',
                  'nbre', 'description',)


class AppartementSerializers(RelationModelSerializer):
    """Apparment."""

    structures = serializers.SerializerMethodField()

    class Meta:
        """Meta."""

        model = Appartement
        fields = ('id', 'intitule',
                  'level',
                  'autre_description',
                  'statut',
                  'immeuble',
                  'structures')

    def get_structures(self, appartement):
        """Create function."""
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
            )
        return StructureAppartmentSerializers(
            structures,
            many=True,
            ).data

    def create(self, validated_data):
        """Create function."""
        structures_data = self.initial_data['structures']
        logger.debug(f' fetching structure data -- {structures_data}')
        appartement = Appartement.objects.create(**validated_data)
        if 'structures' in self.initial_data:
            structures = self.initial_data.get('structures')
            for structure in structures:
                composant_id = structure. \
                    get('composantAppartement', None)
                composant_instance = ComposantAppartement. \
                    objects.get(pk=composant_id)
                structure.pop('composantAppartement')
                structure.pop('appartement')
                StructureAppartement(appartement=appartement,
                                     composantAppartement=composant_instance,
                                     **structure).save()
        appartement.save()
        return appartement
