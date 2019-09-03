import logging

from rest_framework import serializers

from .models import *
from banque.models import Banque
from banque.serializers import BanqueSerializers
from customuser.models import User
from customuser.serializers import UserSerializer
from immeuble.models import Immeuble
from immeuble.serializers import ImmeubleSerializers

logger = logging.getLogger(__name__)


class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    immeubles = serializers.SerializerMethodField()
    banque = BanqueSerializers()
    user = UserSerializer()

    class Meta:
        model = Proprietaire
        fields = ['id', 'mode_paiement', 'numcompte',
                  'pays_residence', 'user', 'banque', 'immeubles']

    def get_immeubles(self, proprietaire):
        immeubles = Immeuble.objects.filter(
            proprietaire=proprietaire,
            )
        return ImmeubleSerializers(
            immeubles,
            many=True,
            context={'request': self.context['request']}
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
        user_data = validated_data.pop('user', None)
        banque_data = validated_data.pop('banque', None)
        if banque_data:
            banque = Banque.objects.get_or_create(**banque_data)[0]
            validated_data['banque'] = banque
        user_instance = User.objects.get(username=user_data['username'])
        try:
            Proprietaire.objects.get(user=user_instance)
        except Proprietaire.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError('Cet utilisateur est déjà un propriétaire')
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
