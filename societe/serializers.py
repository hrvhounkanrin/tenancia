"""RealEstate app serializers."""
from django.db import transaction
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.utils.model_meta import get_field_info

from customuser.models import User
from immeuble.serializers import ImmeubleSerializers

from .models import Mandat, RealEstate, RealEstateUsers


class SocieteSerializer(serializers.ModelSerializer):
    """RealEstate model serializer."""

    class Meta:
        """RealEstate serializer meta."""

        model = RealEstate
        fields = (
            "id",
            "raison_social",
            "num_telephone",
            "adresse",
            "num_carte_professionnel",
            "numero_ifu",
            "date_delivrance",
        )

    @transaction.atomic
    def update(self, instance, validated_data):
        """RealEstate serializer update."""
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    @transaction.atomic
    def create(self, validated_data):
        """
        Create societe.

        :rtype:RealEstate
        """

        user = self.context["request"].user
        nb_real_estate = RealEstate.objects.filter(created_by=user.id).count()
        if nb_real_estate > 0:
            raise serializers.ValidationError(
                "Vous avez déjà configuré une agence immobilière"
            )

        societe = RealEstate.objects.create(
            **validated_data, created_by=user, modified_by=user
        )
        realEstateUser = RealEstateUsers(societe=societe, user=user)
        realEstateUser.save()
        return societe
        """
        if "users" in self.initial_data:
            users = self.initial_data.get("users")
            for user in users:
                id = user.get("id")
                user_instance = User.objects.get(pk=id)
                RealEstateUsers(societe=societe, user=user_instance).save()
        societe.save()
        return societe
        """


class SocieteUsersSerializer(serializers.ModelSerializer):
    """SocieteUser serializer."""

    id = serializers.ReadOnlyField(source="societe.id")
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        """Societeuser meta."""

        model = RealEstateUsers
        fields = ("id", "name")


class MandatSerializer(serializers.ModelSerializer):
    """Mandat model serializer."""

    immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source="RealEstate",
        queryset=RealEstate.objects.all(),
        write_only=True,
        required=False,
    )
    societe = SocieteSerializer(read_only=True)
    societe_id = serializers.PrimaryKeyRelatedField(
        source="RealEstate",
        queryset=RealEstate.objects.all(),
        write_only=True,
        required=False,
    )

    class Meta:
        """Mandat model serializer meta."""

        model = Mandat
        fields = (
            "id",
            "reference_mandat",
            "date_debut",
            "duree",
            "date_echeance",
            "tacite_reconduction",
            "taux_commission",
            "mandant_physique",
            "immeuble",
            "immeuble_id",
            "societe",
            "societe_id",
        )

    @transaction.atomic
    def create(self, validated_data):
        """
        Create mandat.

        :rtype: Mandat
        """
        immeuble = validated_data.pop("Immeuble", None)
        societe = validated_data.pop("RealEstate", None)
        mandat_instance = Mandat.objects.create(
            immeuble=immeuble, societe=societe, **validated_data
        )
        return mandat_instance

    @transaction.atomic
    def update(self, instance, validated_data):
        """Update mandat."""
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
