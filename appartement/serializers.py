"""Housing app serializers."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers

from immeuble.models import Immeuble

from .models import Appartement, StructureAppartement, TypeDependence


class TypeDependenceSerializers(serializers.ModelSerializer):
    """TypeDependence(Housing dependecy type) serializer."""

    class Meta:
        """TypeDependence serializer meta."""

        model = TypeDependence
        fields = "__all__"


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """Housing decustom_exception_handlerpendecies of specfic housing."""

    # typedependence = TypeDependenceSerializers(read_only=True)
    typedependence = serializers.SerializerMethodField()
    typeDependence_id = serializers.PrimaryKeyRelatedField(
        source="TypeDependence",
        queryset=TypeDependence.objects.all(),
        write_only=True,
    )

    class Meta:
        """StructureAppartement meta."""

        model = StructureAppartement
        fields = [
            "appartement",
            "typedependence",
            "typeDependence_id",
            "nbre",
            "description",
        ]

    def get_typedependence(self, structureAppart):
        return structureAppart.typedependence.libelle


class AppartementSerializers(serializers.ModelSerializer):
    """Housing serializer."""

    structures = serializers.SerializerMethodField()
    # immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source="Immeuble",
        queryset=Immeuble.objects.all(),
        write_only=True,
    )

    class Meta:
        """Housing serializer meta."""

        model = Appartement
        fields = (
            "id",
            "intitule",
            "level",
            "autre_description",
            "statut",
            "immeuble_id",
            "structures",
        )  # 'immeuble',

    def get_structures(self, appartement):
        """Get housing dependecies.

        :param appartement:
        :return:
        """
        structures = StructureAppartement.objects.filter(
            appartement=appartement.id,
        )
        data = StructureAppartmentSerializers(
            structures,
            many=True,
        ).data
        print(data)
        return data

    @transaction.atomic
    def create(self, validated_data):
        """Create housing.

        :rtype: Appartement
        """
        immeuble = validated_data.pop("Immeuble", None)
        logement_instance = Appartement.objects.create(
            immeuble=immeuble, **validated_data
        )
        if "structures" in self.initial_data:
            structures = self.initial_data.get("structures")
            for structure in structures:
                dependency_id = structure.pop("typeDependence_id", None)
                try:
                    dependency_instance = TypeDependence.objects.get(id=dependency_id)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(
                        "Il y a une dépendence qui n'existe pas."
                    )
                structure.pop("appartement", None)
                StructureAppartement(
                    appartement=logement_instance,
                    typedependence=dependency_instance,
                    **structure,
                ).save()
            logement_instance.save()
        return logement_instance

    # TODO : Check whether Component exist before saving structure
    @transaction.atomic
    def update(self, instance, validated_data):
        """Update housing."""
        instance.intitule = validated_data["intitule"]
        instance.level = validated_data["level"]
        instance.autre_description = validated_data["autre_description"]
        instance.statut = validated_data["statut"]
        instance.save()
        if "structures" in self.initial_data:
            StructureAppartement.objects.filter(appartement__id=instance.id).delete()
            structures = self.initial_data.get("structures")
            for structure in structures:
                structure.pop("appartement", None)
                print(structure)
                # StructureAppartement(appartement=instance, **structure).save()
        return instance


class ClonerAppartementSerializer(serializers.Serializer):
    nb = serializers.IntegerField(default=1)
    appartement_id = serializers.IntegerField()
    immeuble_id = serializers.IntegerField(write_only=True)
    appartements = AppartementSerializers(read_only=True, many=True)

    @transaction.atomic
    def create(self, validated_data):
        try:
            appartement = Appartement.objects.get(pk=validated_data["appartement_id"])
            print(f"appartement: {appartement}")
            immeuble = Immeuble.objects.get(pk=validated_data["immeuble_id"])
            print(f"immeuble: {immeuble}")
        except ObjectDoesNotExist:
            raise serializers.ValidationError(
                "L'appartement que vous voulez reproduire n'existe pas."
            )

        user = self.context["request"].user
        appartements = []
        appartement_fields = list(appartement.__dict__.keys())
        appartement_fields = [
            f
            for f in appartement_fields
            if f not in ["id", "created_by_id", "modified_by_id", "_state"]
        ]
        for i in range(validated_data["nb"]):
            new_appartement = Appartement()
            for field in list(appartement_fields):

                field_name_val = getattr(appartement, field)
                # print(f'field_value: {field_name_val}')
                setattr(new_appartement, field, field_name_val)
            new_appartement.immeuble = immeuble
            new_appartement.intitule = get_random_string(8).upper()
            new_appartement.created_by = user
            appartements.append(new_appartement)
        [m.save() for m in appartements]
        structures = StructureAppartement.objects.filter(appartement=appartement)
        for m in appartements:
            [
                StructureAppartement(
                    appartement=m,
                    typedependence=s.typedependence,
                    nbre=s.nbre,
                    description=s.description,
                ).save()
                for s in structures
            ]

        return {
            "nb": validated_data["nb"],
            "appartement_id": validated_data["appartement_id"],
            "appartements": appartements,
        }
