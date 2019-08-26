# -*- coding: UTF-8 -*-
from  .models import Client
from rest_framework import serializers
from rest_framework.utils.model_meta import get_field_info
from banque.serializers import BanqueSerializers
from banque.models import Banque
from customuser.serializers import UserSerializer
from customuser.models import User


class ClientSerializer(serializers.ModelSerializer):
    """
        Serializer for class Client
     """
    #contrats = serializers.SerializerMethodField()
    banque = BanqueSerializers(read_only=True)
    banque_id = serializers.PrimaryKeyRelatedField(source='Banque', queryset=Banque.objects.all(), write_only=True, )
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(source='User', queryset=User.objects.all(), write_only=True, )
    class Meta:
        model = Client
        fields = ('id', 'profession', 'mode_paiement', 'ice_contact', 'ice_number', 'ice_relation'
                  , 'user', 'user_id', 'banque', 'banque_id', )


    def create(self, validated_data):
        user_instance = validated_data.pop('User', None)
        banque_instance = validated_data.pop('Banque', None)
        try:
            Client.objects.get(user=user_instance)
        except Client.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("Cet utilisateur est déjà un client")
        return Client.objects.create(user=user_instance, banque=banque_instance, **validated_data)

    def update(self, instance, validated_data):
        if instance.user.id != self.initial_data.get('user_id', None):
            raise serializers.ValidationError("Impossible de changer l'objet user du client")
        info = get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance