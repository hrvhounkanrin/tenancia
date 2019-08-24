# -*- coding: UTF-8 -*-
from django.db import transaction
from rest_framework import serializers, exceptions
from customuser.models import  User
from .models import *


class SocieteSerializer(serializers.ModelSerializer):
    """ Reglement serializer"""

    class Meta:
        model = Societe
        fields = '__all__'

    @transaction.atomic
    def update(self, instance, validated_data):
        SocieteUsers.objects.filter(societe=instance).delete()
        users = self.initial_data.get("users")
        for user in users:
            id = user.get("id")
            """Récupérer l'id de l'utilsateur et créer l'ajouter à la société"""
            #new_user = User.objects.get(pk=id)
            new_user = User()
            SocieteUsers(societe=instance, user=new_user).save()

        instance.__dict__.update(**validated_data)
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
