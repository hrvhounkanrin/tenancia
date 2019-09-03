"""Client Seriazlizers."""
from rest_framework import serializers

from banque.models import Banque
from banque.serializers import BanqueSerializers
from client.models import Client
from contrat.models import Contrat
from contrat.serializers import ContratSerializers
from customuser.models import User
from customuser.serializers import UserSerializer


class ClientSerializer(serializers.ModelSerializer):
    """Serializer for class Client."""

    contrats = serializers.SerializerMethodField()
    banque = BanqueSerializers()
    user = UserSerializer()

    class Meta:
        """Meta Class."""

        model = Client
        fields = ('id', 'nom', 'prenom',
                  'profession',
                  'mode_paiement',
                  'ice_contact',
                  'ice_number',
                  'ice_relation',
                  'user',
                  'banque',
                  'contrats')

    def get_contrats(self, client):
        """String.:return."""
        contrats = Contrat.objects.filter(
            client=client,
            )
        return ContratSerializers(
            contrats,
            many=True,
            context={'request': self.context['request']}
            ).data

    def get_user(self, client):
        """Get user."""
        return UserSerializer(
            client.user,
            many=False,
            context={'request': self.context['request']}
            ).data

    def get_banque(self, client):
        """Get banque."""
        return BanqueSerializers(
            client.banque,
            many=False,
            context={'request': self.context['request']}
            ).data

    def create(self, validated_data):
        """Create function."""
        user_data = validated_data.pop('user', None)
        banque_data = validated_data.pop('banque', None)
        if banque_data:
            banque = Banque.objects.get_or_create(**banque_data)[0]
            validated_data['banque'] = banque
        user_instance = User.objects. \
            get(username=user_data['username'])
        try:
            Client.objects.get(user=user_instance)
        except Client.DoesNotExist:
            pass
        else:
            raise serializers. \
                ValidationError('Cet utilisateur est déjà un client tenancia')
        return Client.objects. \
            create(user=user_instance, **validated_data)
