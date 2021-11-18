"""Immeuble app serializer."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers
from appartement.models import Appartement
from appartement.serializers import AppartementSerializers, ClonerAppartementSerializer
from proprietaire.models import Proprietaire
from societe.models import RealEstateUsers, RealEstate
from .models import AutoName, Immeuble


class ImmeubleSerializers(serializers.ModelSerializer):
    """Immeuble serializer."""

    # proprietaire = ProprietaireSerializers(read_only=True)
    appartements = serializers.SerializerMethodField()
    proprietaire_id = serializers.PrimaryKeyRelatedField(
        source="Proprietaire", queryset=Proprietaire.objects.all(), write_only=True, required=False
    )
    realestate_id = serializers.PrimaryKeyRelatedField(
        source="RealEstate", queryset=RealEstate.objects.all(), write_only=True, required=False
    )
    class Meta:
        """Immeuble serializer meta."""

        model = Immeuble
        fields = (
            "id",
            "intitule",
            "description",
            "adresse",
            "jour_emission_facture",
            "jour_valeur_facture",
            "ville",
            "quartier",
            "pays",
            "longitude",
            "latitude",
            "ref_immeuble",
            "proprietaire_id",
            "realestate_id",
            "appartements",
        )  #'proprietaire',

    def get_appartements(self, immeuble):
        appartements = Appartement.objects.filter(immeuble_id=immeuble.id)
        serialized_appartements = AppartementSerializers(data=appartements, many=True)
        serialized_appartements.is_valid()
        return serialized_appartements.data

    def create(self, validated_data):
        """
        Create Immeuble.

        :rtype: Immeuble
        """
        proprietaire = validated_data.pop("Proprietaire", None)
        realEstate = validated_data.pop("RealEstate", None)
        if not proprietaire and not realEstate:
            raise serializers.ValidationError("Il manque le propriétaire ou l'agence immobilière.")
        # noinspection PyPackageRequirements
        user_count = RealEstateUsers.objects.filter(user=self.context["request"].user,
                                            societe=realEstate).count()

        if realEstate and user_count <= 0:
            raise serializers.ValidationError("Not authorized")

        return Immeuble.objects.create(proprietaire=proprietaire,
                                       realestate=realEstate, **validated_data)

class LigthImmeubleSerializers(serializers.ModelSerializer):
    """Immeuble serializer."""

    class Meta:
        """Ligth Immeuble serializer meta."""

        model = Immeuble
        fields = (
            "id",
            "intitule",
            "description",
            "adresse",
            "jour_emission_facture",
            "jour_valeur_facture",
            "ville",
            "quartier",
            "pays",
            "longitude",
            "latitude",
            "ref_immeuble",
        )



    def create(self, validated_data):
        raise serializers.ValidationError("Not implemented")

    def update(self, validated_data):
        raise serializers.ValidationError("Not implemented")

class ClonerImmeubleSerializer(serializers.Serializer):
    nb = serializers.IntegerField(default=1)
    immeuble_id = serializers.IntegerField()
    immeuble = ImmeubleSerializers(read_only=True)

    class Meta:
        read_only_fields = "immeuble"

    @transaction.atomic
    def create(self, validated_data):
        try:
            immeuble = Immeuble.objects.get(pk=validated_data["immeuble_id"])
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "L'immeuble que vous voulez cloner n'existe pas."
            )

        apprtments = immeuble.appartement_set.all()
        user = self.context["request"].user

        new_immeubles = []
        immeuble_fields = list(immeuble.__dict__.keys())
        immeuble_fields = [
            f
            for f in immeuble_fields
            if f not in ["id", "created_by_id", "modified_by_id", "_state"]
        ]
        for i in range(validated_data["nb"]):
            new_immeuble = Immeuble()
            for field in list(immeuble_fields):
                field_name_val = getattr(immeuble, field)
                setattr(new_immeuble, field, field_name_val)
            new_immeuble.intitule = AutoName.objects.random()
            new_immeuble.created_by = user
            new_immeubles.append(new_immeuble)
        [m.save() for m in new_immeubles]

        for im in new_immeubles:
            for app in apprtments:
                appartment_data = {
                    "immeuble_id": im.id,
                    "appartement_id": app.id,
                    "nb": 1,
                }
                appartment_serializer = ClonerAppartementSerializer(
                    data=appartment_data, context=self.context
                )
                appartment_serializer.is_valid()
                appartment_serializer.save()
        serialized_immeuble = ImmeubleSerializers(data=new_immeuble)
        serialized_immeuble.is_valid()
        return {
            "nb": validated_data["nb"],
            "immeuble_id": validated_data["immeuble_id"],
            "immeuble": new_immeuble,
        }


