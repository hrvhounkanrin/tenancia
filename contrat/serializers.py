"""Contrat Serializers."""
from calendar import mdays
from datetime import date, datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info

from appartement.models import Appartement
from appartement.serializers import AppartementSerializers
from client.models import Client
from client.serializers import ClientSerializer
from quittance.models import Quittance
from tools.sms import Sms
from tools.utils import truncated_uuid4
from quittance.serializers import QuittanceSerializers
from .models import Accesoireloyer, Contrat, ContratAccessoiresloyer


class AccesoireloyerSerializers(serializers.ModelSerializer):
    """Serializers for model Accesoireloyer."""

    class Meta:
        """AccesoireloyerSerializers meta."""

        model = Accesoireloyer
        fields =('id', 'libelle', 'utilite')


class ContratSerializers(serializers.ModelSerializer):
    """Contrat serializer."""

    accessoires = serializers.SerializerMethodField()
    client = ClientSerializer(
        read_only=True,
    )
    client_id = serializers.PrimaryKeyRelatedField(
        source="Client",
        queryset=Client.objects.all(),
        write_only=True,
    )
    appartement = AppartementSerializers(read_only=True)
    appartement_id = serializers.PrimaryKeyRelatedField(
        source="Appartement",
        queryset=Appartement.objects.all(),
        write_only=True,
    )
    reference_bail = serializers.CharField(read_only=True)

    class Meta:
        """Contrat serializer meta."""

        model = Contrat
        fields = (
            "id",
            "date_signature",
            "reference_bail",
            "client_accord",
            "date_accord_client",
            "jour_emission",
            "prochaine_echeance",
            "date_effet",
            "periodicite",
            "duree",
            "montant_bail",
            "nb_avance",
            "nb_prepaye",
            "statut",
            "observation",
            "tacite_reconduction",
            "accessoires",
            "client",
            "client_id",
            "appartement",
            "appartement_id",
        )

    def get_accessoires(self, contrat):
        """Get accessoires of contrat."""
        accessoires = ContratAccessoiresloyer.objects.filter(
            contrat=contrat.id,
        )
        return ContratAccessoiresloyerSerializers(
            accessoires,
            context=self.context,
            many=True,
        ).data

    @transaction.atomic
    def create(self, validated_data):
        """
        Create contrat.

        :rtype: object
        """
        appartement_instance = validated_data.pop("Appartement", None)
        if appartement_instance.statut != 'LIBRE':
            raise serializers.ValidationError("Impossible de mettre un contrat sur un appartement {}".format(appartement_instance.statut))

        print(f"validated_data: {validated_data}")
        client_instance = validated_data.pop("Client", None)

        date_effet = validated_data["date_effet"]
        jour_emission = validated_data["jour_emission"]
        prochaine_echeance = date(
            date_effet.year, date_effet.month, jour_emission
        ) + relativedelta(months=+1)
        contrat = Contrat.objects.create(
            reference_bail=truncated_uuid4(),
            client_accord=False,
            prochaine_echeance=prochaine_echeance,
            client=client_instance,
            appartement=appartement_instance,
            created_by=self.context["request"].user,
            **validated_data,
        )
        if "accessoires" in self.initial_data:
            accessoires = self.initial_data.get("accessoires")
            for accessoire in accessoires:
                accessoire_instance = Accesoireloyer.objects.get(
                    pk=accessoire.get("id", None)
                )
                accessoire.pop("id", None)
                ContratAccessoiresloyer(
                    contrat_id=contrat.id,
                    accesoireloyer_id=accessoire_instance.id,
                    montant=accessoire.get("montant", None),
                    is_peridic=accessoire.get("is_peridic", False)
                ).save()
        contrat.save()
        appartement_instance.statut = 'RESERVE'
        appartement_instance.save(update_fields=['statut'])
        # sms = Sms()
        sms_client = Sms()
        # print(sms_client)
        sms_client.contrat_emis_sms.delay(
            {
                "first_name": contrat.client.user.first_name,
                "phone_number": contrat.client.user.phone_number,
                "reference": contrat.reference_bail,
                "montant_bail": contrat.montant_bail,
                "date_effet": contrat.date_effet,
            }
        )
        return contrat

    def update(self, instance, validated_data):
        """Update contrat."""
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance["modified_by"] = self.context["request"].user
        instance.save()
        return instance



class AgreementSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    client_accord = serializers.BooleanField()


    @transaction.atomic
    def create(self, validated_data):
        raise NotImplementedError("`create()` must be implemented.")

    @transaction.atomic
    def update(self, instance, validated_data):

        if instance.client.user_id != self.context["request"].user.id:
            raise serializers.ValidationError(
                "Vous n'avez pas l'autorisation pour valider ce contrat."
            )

        if instance.client_accord:
            raise serializers.ValidationError("Ce contrat a été déjà accepté.")

        instance.client_accord = validated_data["client_accord"]
        instance.modified_by = self.context["request"].user
        instance.date_accord_client = datetime.today()
        if validated_data["client_accord"]:
            instance.statut = "CONTRAT ACCEPTE"
            instance.observation = "CONTRAT ACCEPTE PAR LE CLIENT"
        else:
            instance.observation = "CONTRAT REFUSE PAR LE CLIENT"

        instance.save(update_fields=['statut', 'observation', 'client_accord', 'modified_by', 'date_accord_client'])
        # Un contrat accepté est un contrat dont l'appartment devient occuper
        appartement_instance = instance.appartement
        appartement_instance.statut = 'OCCUPE'
        appartement_instance.save(update_fields=['statut'])

        montant_global = 0

        if validated_data["client_accord"]:
            contrat = instance
            # récupération des frais accessoires sur le contrat
            accessoires = ContratAccessoiresloyer.objects.filter(contrat=contrat)
            quittances = []
            # création des quittances de frais accessoires
            for acc in accessoires:
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature=acc.accesoireloyer.libelle,
                    contrat=contrat,
                    montant=acc.montant,
                    lessor_user_id=appartement_instance.immeuble.proprietaire_id,
                    tenant_user_id=instance.client_id
                )
                quittances.append(quittance)
                # montant_global = montant_global + acc.montant
            # création des quittance d'avance sur loyer
            for i in range(instance.nb_avance):
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature="AVANCE SUR LOYER",
                    contrat=contrat,
                    montant=instance.montant_bail,
                    lessor_user_id=appartement_instance.immeuble.proprietaire_id,
                    tenant_user_id=instance.client_id

                )
                quittances.append(quittance)
                montant_global = montant_global + acc.montant
            # création des quittance de prépayés
            for i in range(instance.nb_prepaye):
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature="QUITTANCE DE LOYER PREPAYE",
                    contrat=contrat,
                    montant=instance.montant_bail,
                    lessor_user_id=appartement_instance.immeuble.proprietaire_id,
                    tenant_user_id=instance.client_id
                )
                quittances.append(quittance)

            [model.save() for model in quittances]
        # alert sms validation
        contrat_data = {
            "first_name": instance.created_by.first_name,
            "reference": instance.reference_bail,
            "created_at": instance.created_at,
            "client_accord": instance.client_accord,
            "phone_number": instance.created_by.phone_number,
            "client_name": f"{instance.client.user.first_name} {instance.client.user.last_name}",
        }
        sms_client = Sms()
        # sms_client.contrat_valide_sms.delay
        montant_global = sum([quittance.montant for quittance in quittances])
        if instance.client_accord:
            quittance_data = {
                "first_name": instance.client.user.first_name,
                "reference": instance.reference_bail,
                "montant_global": montant_global,
                "phone_number": instance.client.user.phone_number,
                "client_accord": instance.client_accord,
            }
            # sms_client.contrat_valide_client_sms.delay(quittance_data)
        return instance

"""
class AgreementSerializer(serializers.ModelSerializer):
    contrat_id = serializers.PrimaryKeyRelatedField(
        source="Contrat",
        queryset=Contrat.objects.all(),
        write_only=True,
    )
    contrat = ContratSerializers(
        read_only=True,
    )
    client_accord = serializers.BooleanField(write_only=True)
    quittances = serializers.SerializerMethodField()

    def get_quittances(self, contrat_id):
        return  contrat_id

    @transaction.atomic
    def create(self, validated_data):
        raise NotImplementedError("`create()` must be implemented.")

    @transaction.atomic
    def update(self, instance, validated_data):

        if instance.client.user_id != self.context["request"].user.id:
            raise serializers.ValidationError(
                "Vous n'avez pas l'autorisation pour valider ce contrat."
            )

        if instance.client_accord:
            raise serializers.ValidationError("Ce contrat a été déjà accepté.")

        instance.client_accord = validated_data["client_accord"]
        instance.modified_by = self.context["request"].user
        instance.date_accord_client = datetime.today()
        if validated_data["client_accord"]:
            instance.statut = "CONTRAT ACCEPTE"
            instance.observation = "CONTRAT ACCEPTE PAR LE CLIENT"
        else:
            instance.observation = "CONTRAT REFUSE PAR LE CLIENT"

        instance.save(update_fields=['statut', 'observation', 'client_accord', 'modified_by', 'date_accord_client'])
        # Un contrat accepté est un contrat dont l'appartment devient occuper
        appartement_instance = instance.appartement
        appartement_instance.statut = 'OCCUPE'
        appartement_instance.save(update_fields=['statut'])

        montant_global = 0
        if validated_data["client_accord"]:
            contrat = instance
            # récupération des frais accessoires sur le contrat
            accessoires = ContratAccessoiresloyer.objects.filter(contrat=contrat)
            quittances = []
            # création des quittances de frais accessoires
            for acc in accessoires:
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature=acc.accesoireloyer.libelle,
                    contrat=contrat,
                    montant=acc.montant,
                )
                quittances.append(quittance)
                # montant_global = montant_global + acc.montant
            # création des quittance d'avance sur loyer
            for i in range(instance.nb_avance):
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature="AVANCE SUR LOYER",
                    contrat=contrat,
                    montant=instance.montant_bail,
                )
                quittances.append(quittance)
                montant_global = montant_global + acc.montant
            # création des quittance de prépayés
            for i in range(instance.nb_prepaye):
                quittance = Quittance(
                    reference=truncated_uuid4(),
                    date_emission=date.today(),
                    date_valeur=contrat.date_effet,
                    debut_periode=contrat.date_effet,
                    fin_periode=contrat.date_effet,
                    nature="QUITTANCE DE LOYER PREPAYE",
                    contrat=contrat,
                    montant=instance.montant_bail,
                )
                quittances.append(quittance)

            [model.save() for model in quittances]
        # alert sms validation
        contrat_data = {
            "first_name": instance.created_by.first_name,
            "reference": instance.reference_bail,
            "created_at": instance.created_at,
            "client_accord": instance.client_accord,
            "phone_number": instance.created_by.phone_number,
            "client_name": f"{instance.client.user.first_name} {instance.client.user.last_name}",
        }
        sms_client = Sms()
        # sms_client.contrat_valide_sms.delay
        montant_global = sum([quittance.montant for quittance in quittances])
        if instance.client_accord:
            quittance_data = {
                "first_name": instance.client.user.first_name,
                "reference": instance.reference_bail,
                "montant_global": montant_global,
                "phone_number": instance.client.user.phone_number,
                "client_accord": instance.client_accord,
            }
            # sms_client.contrat_valide_client_sms.delay(quittance_data)
        return instance
"""

class ContratAccessoiresloyerSerializers(serializers.ModelSerializer):
    """ContratAccessoireloyer serializer."""

    accesoireloyer = AccesoireloyerSerializers(read_only=True)
    accesoireloyer_id = serializers.PrimaryKeyRelatedField(
        source="Accesoireloyer",
        queryset=Accesoireloyer.objects.all(),
        write_only=True,
    )

    class Meta:
        """ContratAccessoireloyer meta."""

        model = ContratAccessoiresloyer
        fields = (
            "contrat",
            "accesoireloyer",
            "accesoireloyer_id",
            "montant",
            "devise",
            "statut",
            "devise",
            "description",
        )
