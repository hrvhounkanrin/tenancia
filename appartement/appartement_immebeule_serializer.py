"""Appartement immeuble serializer."""
from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject
from appartement.models import Appartement
from immeuble.serializers import ImmeubleSerializers
from collections import OrderedDict

class AppartementImmeubleSerializers(serializers.ModelSerializer):
    """Appartement serializer."""
    immeuble_intitule = serializers.SerializerMethodField()
    immeuble_id = serializers.SerializerMethodField()
    jour_emission_facture = serializers.SerializerMethodField()
    jour_valeur_facture = serializers.SerializerMethodField()
    ville = serializers.SerializerMethodField()
    quartier = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    ref_immeuble = serializers.SerializerMethodField()
    ref_immeuble = serializers.SerializerMethodField()
    proprietaire = serializers.SerializerMethodField()
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
            'immeuble_intitule',
            'jour_emission_facture',
            'jour_valeur_facture',
            'ville',
            'quartier',
            'longitude',
            'latitude',
            'ref_immeuble',
            'proprietaire'
        )
        read_only_fields = ['account_name']

    def get_immeuble_id(self, appartement):
        return appartement.immeuble.id

    def get_immeuble_intitule(self, appartement):
        return appartement.immeuble.intitule

    def get_jour_emission_facture(self, appartement):
        return appartement.immeuble.jour_emission_facture

    def get_jour_valeur_facture(self, appartement):
        return appartement.immeuble.jour_valeur_facture

    def get_ville(self, appartement):
        return appartement.immeuble.ville

    def get_quartier(self, appartement):
        return appartement.immeuble.quartier

    def get_longitude(self, appartement):
        return appartement.immeuble.longitude

    def get_latitude(self, appartement):
        return appartement.immeuble.latitude

    def get_ref_immeuble(self, appartement):
        return appartement.immeuble.ref_immeuble

    def get_proprietaire(self, appartement):
        if appartement.immeuble.realestate:
            return "{}".format(appartement.immeuble.realestate.raison_social)
        return "{} {} ({})".format(appartement.immeuble.proprietaire.user.first_name,
                                   appartement.immeuble.proprietaire.user.last_name,
                                   appartement.immeuble.proprietaire.phone_number)