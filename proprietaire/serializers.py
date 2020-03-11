# -*- coding: UTF-8 -*-
"""Proprietaire serializer.py."""
import logging

from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info

from . models import Proprietaire
from banque.models import Banque
from banque.serializers import BanqueSerializers
from customuser.models import User
from customuser.serializers import UserSerializer
logger = logging.getLogger(__name__)


class ProprietaireSerializers(serializers.ModelSerializer):
    """Poprietaire model serializer."""

    banque = BanqueSerializers(read_only=True)
    banque_id = serializers.PrimaryKeyRelatedField(
        source='Banque', queryset=Banque.objects.all(), write_only=True, )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        source='User', queryset=User.objects.all(), write_only=True, )

    class Meta:
        """Proprietaire model meta class."""

        model = Proprietaire
        fields = ['id', 'mode_paiement', 'numcompte', 'pays_residence',
                  'user', 'user_id', 'banque', 'banque_id']

    def get_user(self, proprietaire):
        """Get user model of proprietaire."""
        return UserSerializer(
            proprietaire.user,
            many=False,
            context={'request': self.context['request']}
        ).data

    def get_banque(self, proprietaire):
        """Get banque of designated proprietaire."""
        return BanqueSerializers(
            proprietaire.banque,
            many=False,
            context={'request': self.context['request']}
        ).data

    def create(self, validated_data):
        """
        Create proprietaire.

        :rtype: Proprietaire instance
        """
        user_instance = validated_data.pop('User', None)
        banque_instance = validated_data.pop('Banque', None)
        try:
            Proprietaire.objects.get(user=user_instance)
        except Proprietaire.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError(
                'Cet utilisateur est déjà un propriétaire')
        return Proprietaire.objects.create(
            **validated_data, user=user_instance, banque=banque_instance)

    def update(self, instance, validated_data):
        """Update proprietaire serializer."""
        if instance.user.id != self.initial_data.get(
                'user_id', None):
            raise serializers.ValidationError(
                "Impossible de changer l'objet user du propriétaire")
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
