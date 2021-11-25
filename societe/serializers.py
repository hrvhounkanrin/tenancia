"""RealEstate app serializers."""
import uuid
import logging
from datetime import datetime, timedelta
from django.db import transaction
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info
from django.conf import settings
from immeuble.serializers import LigthImmeubleSerializers
from immeuble.models import Immeuble
from .models import Mandat, RealEstate, RealEstateUsers
logger = logging.getLogger(__name__)

class SocieteSerializer(serializers.ModelSerializer):
    """RealEstate model serializer."""
    logo_url = serializers.SerializerMethodField('get_logo_url')
    class Meta:
        """RealEstate serializer meta."""

        model = RealEstate
        fields = (
            "id",
            "raison_social",
            "num_telephone",
            "adresse",
            "num_carte_professionnel",
            "mode_recouvrement",
            "numero_ifu",
            "date_delivrance",
            "logo",
            "logo_url"
        )
    def get_logo_url(self, societe):
        return f"{settings.MEDIA_URL}{societe.logo}"
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
                "Vous ne pouvez pas configuré plus d'une agence immobilière."
            )

        societe = RealEstate.objects.create(
            **validated_data, created_by=user, modified_by=user
        )
        RealEstateUsers(societe=societe, user=user, profil='MASTER', is_active=True).save()
        return societe


class SocieteUsersSerializer(serializers.ModelSerializer):
    """SocieteUser serializer."""

    # realestate_id = serializers.ReadOnlyField(source="societe.id")
    # email = serializers.ReadOnlyField(source="user.email")

    class Meta:
        """Societeuser meta."""

        model = RealEstateUsers
        fields = ("societe", "user")

    @transaction.atomic
    def create(self, validated_data):
        """
        Create realEstateUsers.

        :rtype:RealEstateUsers
        """
        check_existing = RealEstateUsers.objects.filter(
            societe=validated_data['societe'],
            user=validated_data['user']).first()
        logger.debug(f"check_existing: {check_existing}")
        if check_existing:
            raise serializers.ValidationError("Cet utilisateur est déjà ajouté à votre agence.")

        user = self.context["request"].user
        logger.debug(f"validated_data: {validated_data}")
        token_exp_date = datetime.now() + timedelta(hours=24)
        # TODO: Send email invitation email to user with token
        realestate_user = RealEstateUsers.objects.create(invitation_token=uuid.uuid1(),
                        token_exp_date=token_exp_date,
                        profil='USER', is_active=False, **validated_data)
        return realestate_user

    @transaction.atomic
    def update(self, instance, validated_data):
        """realEstateUsers serializer update."""
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class MandatSerializer(serializers.ModelSerializer):
    """Mandat model serializer."""

    immeuble = LigthImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(
        source="Immeuble",
        queryset=Immeuble.objects.all(),
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
            "immeuble_id",
            "immeuble",
            "societe",
            "societe_id",
            "owner_name",
            "owner_firstname",
            "owner_phone_number",
            "owner_email"
        )
        depth = 0

    @transaction.atomic
    def create(self, validated_data):
        """
        Create mandat.

        :rtype: Mandat
        """

        immeuble = validated_data.pop("Immeuble", None)
        societe = validated_data.pop("RealEstate", None)
        mandat_count = Mandat.objects.filter(immeuble=immeuble).count()
        if mandat_count > 0:
            raise serializers.ValidationError("Il existe un mandat actif sur cet immeuble")
        mandat_instance = Mandat.objects.create(
            immeuble=immeuble,
            societe=societe,
            created_by=self.context["request"].user,
            **validated_data
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
        instance.modified_by = self.context["request"].user
        instance.save()
        return instance