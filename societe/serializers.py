# -*- coding: UTF-8 -*-
from django.db import transaction
from rest_framework import serializers, exceptions
from rest_framework.utils.model_meta import get_field_info
from customuser.models import  User
from .models import *
from immeuble.models import Immeuble
from immeuble.serializers import ImmeubleSerializers

class SocieteSerializer(serializers.ModelSerializer):
    """ Mandataire serializer"""

    class Meta:
        model = Societe
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validated_data):
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
    id = serializers.ReadOnlyField(source='societe.id')
    name = serializers.ReadOnlyField(source='user.name')

    class Meta:
        model = SocieteUsers
        fields = ('id', 'name')


class MandatSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializers(read_only=True)
    immeuble_id = serializers.PrimaryKeyRelatedField(source='Societe', queryset=Societe.objects.all(), write_only=True,required=False )
    societe = SocieteSerializer(read_only=True)
    societe_id = serializers.PrimaryKeyRelatedField(source='Societe', queryset=Societe.objects.all(), write_only=True,required=False )
    class Meta:
        model = Mandat
        fields = ('id', 'reference_mandat', 'date_debut', 'duree', 'date_echeance','tacite_reconduction','taux_commission', 'mandant_physique',  'immeuble', 'immeuble_id',  'societe', 'societe_id',)


    @transaction.atomic
    def create(self, validated_data):
        immeuble = validated_data.pop('Immeuble', None)
        societe = validated_data.pop('Societe', None)
        mandat_instance = Mandat.objects.create(immeuble=immeuble, societe=societe, **validated_data)
        return mandat_instance

    @transaction.atomic
    def update(self, instance, validated_data):
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

