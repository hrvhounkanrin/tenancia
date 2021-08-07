"""Quittance app serializer."""
import datetime

from rest_framework import serializers

from contrat.models import Contrat, ContratAccessoiresloyer
from contrat.serializers import ContratSerializers

from .models import Quittance


class QuittanceSerializers(serializers.ModelSerializer):
    """Quittance Serializers."""

    class Meta:
        """Quittance serializer meta."""

        model = Quittance
        fields = "__all__"


class FirstQuittanceSerializers(serializers.ModelSerializer):
    """Quittance Serializers."""

    class Meta:
        """Quittance serializer meta."""

        contrat = ContratSerializers(read_only=True)
        contrat_id = serializers.PrimaryKeyRelatedField(
            source="Contrat",
            queryset=Contrat.objects.all(),
            write_only=True,
        )
        model = Quittance
        # fields = '__all__'
        fields = (
            "reference",
            "date_emission",
            "date_valeur",
            "debut_periode",
            "fin_periode",
            "nature",
            "montant",
            "statut",
            "date_statut",
            "contrat",
            "contrat_id",
            "motif_annulation",
            "created_at",
            "modified_at",
        )

    """
    def create(self, validated_data):
        contrat = Contrat.objects.get(pk=self.initial_data['contrat_id'])
        # récupération des frais accessoires sur le contrat
        accessoires = ContratAccessoiresloyer.objects.filter(contrat=contrat)
        quittances = []
        # création des quittances de frais accessoires
        for acc in accessoires:
            quittance = Quittance(reference='reference', date_emission=datetime.date.today(),
                                  date_valeur=contrat.date_effet, debut_periode=contrat.date_effet,
                                  fin_periode=contrat.date_effet, nature=acc.accesoireloyer.libelle,
                                  contrat=contrat, montant=acc.montant)
            quittances.append(quittance)
        print(quittances)
        return [model.save() for model in quittances]
        print(saved_quittances)
        return saved_quittances
    """
