"""Serializers class for Contract."""
from rest_framework import serializers

from contrat.models import Accesoireloyer
from contrat.models import Contrat
from contrat.models import ContratAccessoiresloyer
from tools.serializers import RelationModelSerializer


class AccesoireloyerSerializers(RelationModelSerializer):
    """Serializers for model Accesoireloyer."""

    class Meta:
        """Meta Class."""

        model = Accesoireloyer
        fields = '__all__'


class ContratAccessoiresloyerSerializers(serializers.ModelSerializer):
    """Structure Serializers."""

    accesoireloyer = \
        AccesoireloyerSerializers(read_only=False, is_relation=True)

    class Meta:
        """Meta class."""

        model = ContratAccessoiresloyer
        fields = ('contrat',
                  'accesoireloyer',
                  'montant',
                  'devise',
                  'statut',
                  'devise',
                  'description')


class ContratSerializers(serializers.ModelSerializer):
    """Contract Serializer."""

    accessoires = serializers.SerializerMethodField()

    class Meta:
        """Class Meta."""

        model = Contrat
        fields = ('id', 'reference_bail', 'date_signature',
                  'date_effet', 'periodicite', 'duree',
                  'montant_bail', 'statut', 'observation',
                  'tacite_reconduction',
                  'client', 'appartement', 'accessoires')

    def get_accessoires(self, contrat):
        """Get accessoires."""
        accessoires = ContratAccessoiresloyer.objects.filter(
            contrat=contrat.id,
            )
        return ContratAccessoiresloyerSerializers(
            accessoires,
            many=True,
            ).data

    def create(self, validated_data):
        """Create function."""
        contrat = Contrat.objects.create(**validated_data)
        if 'accessoires' in self.initial_data:
            accessoires = self.initial_data.get('accessoires')
            for accessoire in \
                    accessoires:
                accessoire_id = \
                    accessoire.get('accessoire', None)
                accessoire_instance = Accesoireloyer. \
                    objects.get(pk=accessoire_id)
                accessoire_id = accessoire.pop('accessoire')
                ContratAccessoiresloyer(contrat=contrat,
                                        accesoireloyer=accessoire_instance,
                                        **accessoire).save()
        return contrat
