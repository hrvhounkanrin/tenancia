"""Housing app serializers."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.db.models import Max
from immeuble.models import Immeuble

from .models import Appartement, StructureAppartement, TypeDependence


class TypeDependenceSerializers(serializers.ModelSerializer):
    """TypeDependence(Housing dependecy type) serializer."""

    class Meta:
        """TypeDependence serializer meta."""

        model = TypeDependence
        fields = ('id', 'libelle', 'utilite')


class StructureAppartmentSerializers(serializers.ModelSerializer):
    """Housing decustom_exception_handlerpendecies of specfic housing."""

    typedependence = TypeDependenceSerializers(read_only=True)
    libelle = serializers.SerializerMethodField()
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
            "libelle",
            "typeDependence_id",
            "nbre",
            "superficie",
            "typedependence",
            "description",
        ]

    def get_libelle(self, structureAppart):
        return structureAppart.typedependence.libelle


class AppartementSerializers(serializers.ModelSerializer):
    """Housing serializer."""

    structures = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    quartier = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    immeuble_intitule = serializers.SerializerMethodField()
    proprietaire = serializers.SerializerMethodField()
    proprietaire_phone_number = serializers.SerializerMethodField()
    proprietaire_mail = serializers.SerializerMethodField()
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
            'immeuble',
            "immeuble_id",
            "structures",
            'ville',
            'quartier',
            'longitude',
            'latitude',
            'immeuble_intitule',
            'proprietaire',
            'proprietaire_phone_number',
            'proprietaire_mail'
        )

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
        return data

    def get_ville(self, appartement):
        return appartement.immeuble.ville

    def get_quartier(self, appartement):
        return appartement.immeuble.quartier

    def get_longitude(self, appartement):
        return appartement.immeuble.longitude

    def get_latitude(self, appartement):
        return appartement.immeuble.latitude

    def get_immeuble_intitule(self, appartement):
        return appartement.immeuble.intitule

    def get_proprietaire(self, appartement):
        if appartement.immeuble.proprietaire \
                is None and appartement.immeuble.realestate \
                is None:
            return None
        if appartement.immeuble.proprietaire:
            return "{} {}".format(appartement.immeuble.proprietaire.user.first_name,
                                  appartement.immeuble.proprietaire.user.last_name)
        return appartement.immeuble.realestate.raison_social

    def get_proprietaire_phone_number(self, appartement):
        if appartement.immeuble.proprietaire \
                is None and appartement.immeuble.realestate \
                is None:
            return None
        if appartement.immeuble.proprietaire:
            return appartement.immeuble.proprietaire.phone_number
        return appartement.immeuble.realestate.num_telephone

    def get_proprietaire_mail(self, appartement):
        if appartement.immeuble.proprietaire \
                is None and appartement.immeuble.realestate \
                is None:
            return None

        if appartement.immeuble.proprietaire:
            return appartement.immeuble.proprietaire.user.email
        return appartement.immeuble.realestate.num_telephone

    def __autoname(self, immeuble, level):
        last_intitule = Appartement.objects.filter(immeuble=immeuble, level=level)
        last_intitule = last_intitule.aggregate(Max('intitule'))['intitule__max']
        if last_intitule is None:
            return str(level)+'-A'
        return last_intitule[0:len(last_intitule)-1]+chr(ord(last_intitule[-1]) + 1)

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
                dependency_id = structure.pop("typeDependence_id", None)
                try:
                    dependency_instance = TypeDependence.objects.get(id=dependency_id)
                except ObjectDoesNotExist:
                    raise serializers.ValidationError(
                        "Il y a une dépendence qui n'existe pas."
                    )
                structure.pop("appartement", None)
                StructureAppartement(
                    appartement=instance,
                    typedependence=dependency_instance,
                    **structure,
                ).save()

        return instance


class ClonerAppartementSerializer(serializers.Serializer):
    nbre = serializers.IntegerField(default=1)
    appartement_id = serializers.IntegerField()
    level = serializers.IntegerField()
    immeuble_id = serializers.IntegerField(write_only=True)
    appartements = AppartementSerializers(read_only=True, many=True)

    @transaction.atomic
    def create(self, validated_data):
        try:
            appartement = Appartement.objects.get(pk=validated_data["appartement_id"])
            immeuble = Immeuble.objects.get(pk=validated_data["immeuble_id"])
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
        last_db_name = self.__autoname(immeuble.id, validated_data['level'])
        for i in range(validated_data["nbre"]):
            new_appartement = Appartement()
            for field in list(appartement_fields):

                field_name_val = getattr(appartement, field)
                # print(f'field_value: {field_name_val}')
                setattr(new_appartement, field, field_name_val)
            new_appartement.immeuble = immeuble
            new_appartement.intitule = last_db_name
            new_appartement.level = validated_data['level']
            last_db_name = self.__autoname(immeuble.id, validated_data['level'], last_db_name)
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
                    superficie=s.superficie,
                    description=s.description,
                ).save()
                for s in structures
            ]
        validated_data['appartements'] = appartements
        return {
            "nbre": validated_data["nbre"],
            "level":  validated_data["level"],
            "appartement_id": validated_data["appartement_id"],
            "appartements": appartements,
        }



    def __autoname(self, immeuble_id, level, last_db_name=None):
        if last_db_name is None:
            last_intitule = Appartement.objects.filter(immeuble__id=immeuble_id, level=level)
            last_intitule = last_intitule.aggregate(Max('intitule'))['intitule__max']
            if last_intitule is None:
                return str(level) + '-A'
        else:
            last_intitule = last_db_name
        return last_intitule[0:len(last_intitule) - 1] + chr(ord(last_intitule[-1]) + 1)