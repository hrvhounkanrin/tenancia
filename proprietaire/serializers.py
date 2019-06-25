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
from banque.models import Banque
from . models import *
from customuser.serializers import UserSerializer
logger = logging.getLogger(__name__)

class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    #immeubles = serializers.SerializerMethodField()
    banque = BanqueSerializers()
    #user = UserSerializer()
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='User', queryset=User.objects.all(), write_only=True, )

    #appartements=serializers.SerializerMethodField()
    class Meta:
        model = Proprietaire
        fields = ['id', 'mode_paiement', 'numcompte', 'pays_residence', 'user', 'user_id', 'banque']
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
        instance.mode_paiement = validated_data['mode_paiement']
        instance.numcompte = validated_data['numcompte']
        instance.pays_residence = validated_data['pays_residence']
        if instance.user.id != self.initial_data.get('user_id', None):
            raise serializers.ValidationError("Impossible de changer l'objet user du proprietaire")
        try:
            banque_instance = Banque.objects.get(pk=self.initial_data['banque']['id'])
            instance.banque = banque_instance
        except Banque.DoesNotExist:
            raise serializers.ValidationError("Cette banque n'existe pas.")
        instance.save()
        return instance