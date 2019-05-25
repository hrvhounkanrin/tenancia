import logging
from rest_framework import serializers, exceptions
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from drf_writable_nested import NestedUpdateMixin
from immeuble.serializers import ImmeubleSerializers
#from appartement.serializers import  AppartementSerializers;
from immeuble.models import Immeuble
from customuser.models import User
from customuser.serializers import UserSerializer
from banque.serializers import BanqueSerializers
from tools.serializers import (DictSerializer, AsymetricRelatedField, )
from banque.models import Banque
from . models import *
logger = logging.getLogger(__name__)

class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    #immeubles = serializers.SerializerMethodField()
    banque = BanqueSerializers()
    user = UserSerializer()
    #appartements=serializers.SerializerMethodField()
    class Meta:
        model = Proprietaire
        fields = ['id', 'mode_paiement', 'numcompte', 'pays_residence', 'user', 'banque',]
        #list_serializer_class = DictSerializer


    def get_immeubles(self, proprietaire):
        immeubles = Immeuble.objects.filter(
            proprietaire=proprietaire,
        )
        return ImmeubleSerializers(
            immeubles,
            many=True,

        ).data


    def get_user(self, proprietaire):
        return UserSerializer(
            proprietaire.user,
            many=False,
            context={'request': self.context['request']}
        ).data

    def get_banque(self, proprietaire):
        return BanqueSerializers(
            proprietaire.banque,
            many=False,
            context={'request': self.context['request']}
        ).data

    def create(self, validated_data):
        #print(validated_data)
        user_data = validated_data.pop('user', None)
        banque_data = validated_data.pop('banque', None)
        if banque_data:
            banque = Banque.objects.get_or_create(**banque_data)[0]
            validated_data['banque'] = banque
        user_instance = User.objects.get(email=user_data['email'])
        try:
            Proprietaire.objects.get(user=user_instance)
        except Proprietaire.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("Cet utilisateur est déjà un propriétaire")
        return Proprietaire.objects.create(user=user_instance, **validated_data)

    def update(self, instance, validated_data):
        instance.mode_paiement = validated_data['mode_paiement']
        instance.numcompte = validated_data['numcompte']
        instance.pays_residence = validated_data['pays_residence']
        try:
            banque_instance = Banque.objects.get(pk=self.initial_data['banque']['id'])
            instance.banque = banque_instance
        except Banque.DoesNotExist:
            raise serializers.ValidationError("Cette banque n'existe pas.")
        instance.save()
        return instance