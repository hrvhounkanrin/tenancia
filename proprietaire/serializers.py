# -*- coding: UTF-8 -*-
import logging
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info
from customuser.models import User
from banque.serializers import BanqueSerializers
from banque.models import Banque
from . models import *
from customuser.serializers import UserSerializer
logger = logging.getLogger(__name__)

class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    banque = BanqueSerializers(read_only=True)
    banque_id = serializers.PrimaryKeyRelatedField(source='Banque', queryset=Banque.objects.all(), write_only=True, )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='User', queryset=User.objects.all(), write_only=True, )

    class Meta:
        model = Proprietaire
        fields = ['id', 'mode_paiement', 'numcompte', 'pays_residence', 'user', 'user_id', 'banque', 'banque_id']

    """
    def get_immeubles(self, proprietaire):
        immeubles = Immeuble.objects.filter(
            proprietaire=proprietaire,
        )
        return ImmeubleSerializers(
            immeubles,
            many=True,

        ).data
    """

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
        user = validated_data.pop('User', None)
        banque_data = validated_data.pop('banque', None)
        if banque_data:
            banque = Banque.objects.get_or_create(**banque_data)[0]
            validated_data['banque'] = banque
        try:
            Proprietaire.objects.get(user=user)
        except Proprietaire.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("Cet utilisateur est déjà un propriétaire")
        return Proprietaire.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        if instance.user.id != self.initial_data.get('user_id', None):
            raise serializers.ValidationError("Impossible de changer l'objet user du propriétaire")
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance