"""Quittance app serializer."""
import datetime

from rest_framework import serializers

from contrat.models import Contrat, ContratAccessoiresloyer

from .models import Quittance


class QuittanceSerializers(serializers.ModelSerializer):
    """Quittance Serializers."""
    appartement = serializers.SerializerMethodField()
    lessor = serializers.SerializerMethodField()
    tenant = serializers.SerializerMethodField()
    contrat_detail = serializers.SerializerMethodField()
    class Meta:
        """Quittance serializer meta."""

        model = Quittance
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
            "motif_annulation",
            "appartement",
            "lessor",
            "tenant",
            "contrat_detail"
        )

    def get_appartement(self, quittance):
        appartement = quittance.contrat.appartement
        return dict({
            "intitule": appartement.intitule,
            "immeuble_intitule": appartement.immeuble.intitule,
            "immeuble_address": appartement.immeuble.ville,
            "longitude": appartement.immeuble.longitude,
            "latitude": appartement.immeuble.latitude
        })

    def get_lessor(self, quittance):
        lessor = quittance.contrat.appartement.immeuble.proprietaire
        return dict({
            "first_name": lessor.user.first_name,
            "last_name": lessor.user.last_name,
            "phone_number": lessor.phone_number,
            "email": lessor.user.email,
        })

    def get_tenant(self, quittance):
        tenant = quittance.contrat.client
        return dict({
            "first_name": tenant.user.first_name,
            "last_name": tenant.user.last_name,
            "phone_number": tenant.phone_number,
            "email": tenant.user.email,
        })

    def get_contrat_detail(self, quittance):
        contrat = quittance.contrat
        return dict({
            "reference_bail": contrat.reference_bail,
            "date_effet": contrat.date_effet,
            "statut": contrat.statut
        })


class FirstQuittanceSerializers(serializers.ModelSerializer):
    """Quittance Serializers."""

    class Meta:
        """Quittance serializer meta."""

        # contrat = ContratSerializers(read_only=True)
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
