# -*- coding: UTF-8 -*-
"""Societe app serializers."""
from django.db import transaction
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info

from .models import Mandat
from .models import Societe
from .models import SocieteUsers
from customuser.models import User
from immeuble.serializers import ImmeubleSerializers


class SocieteSerializer(serializers.ModelSerializer):
    """Societe model serializer."""

    class Meta:
        """Societe serializer meta."""

        model = Societe
        fields = "__all__"

    @transaction.atomic
    def update(self, instance, validated_data):
        """Societe serializer update."""
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

        :rtype:Societe
        """
        societe = Societe.objects.create(**validated_data)
        if "users" in self.initial_data:
            users = self.initial_data.get("users")
            for user in users:
                id = user.get("id")
                user_instance = User.objects.get(pk=id)
                SocieteUsers(societe=societe, user=user_instance).save()
        societe.save()
        return societe


class SocieteUsersSerializer(serializers.ModelSerializer):
    """SocieteUser serializer."""

    id = serializers.ReadOnlyField(source="societe.id")
    name = serializers.ReadOnlyField(source="user.name")

    class Meta:
        """Societeuser meta."""

        model = SocieteUsers
        fields = ("id", "name")


class MandatSerializer(serializers.ModelSerializer):
    """Mandat model serializer."""

    immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source="Societe",
        queryset=Societe.objects.all(),
        write_only=True,
        required=False,
    )
    societe = SocieteSerializer(read_only=True)
    societe_id = serializers.PrimaryKeyRelatedField(
        source="Societe",
        queryset=Societe.objects.all(),
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
        societe = validated_data.pop("Societe", None)
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
