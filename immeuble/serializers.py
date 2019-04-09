from appartement.serializers import (AppartementSerializers,)
from rest_framework import serializers, exceptions
from .models import *
from tools.serializers import RelationModelSerializer
from appartement.models import Appartement


class ImmeubleSerializers(RelationModelSerializer):
    appartements = serializers.SerializerMethodField()
    class Meta:
        model = Immeuble
        #fields = '__all__'
        fields = ('intitule', 'description', 'adresse', 'proprietaire', 'jour_emission_facture',
                  'jour_valeur_facture', 'ville', 'quartier', 'pays', 'longitude', 'latitude', 'ref_immeuble', 'appartements')

    def get_appartements(self, immeuble):
        appartements = Appartement.objects.filter(
            immeuble=immeuble,
        )
        return AppartementSerializers(
            appartements,
            many=True,
            context={'request': self.context['request']}
        ).data


    """
    def create(self, validated_data):
        immeuble_data = validated_data.pop('immeuble')
        immeuble_instance = Immeuble.objects.get(pk=immeuble_data['username'])

        try:
            Appartement.objects.get(user=user_instance)
        except Proprietaire.DoesNotExist:
            pass
        else:
            raise serializers.ValidationError("Cet utilisateur est déjà un propriétaire")
        return Appartement.objects.create(immeuble=immeuble_instance, **validated_data)
    """