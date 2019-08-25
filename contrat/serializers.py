# -*- coding: UTF-8 -*-
from rest_framework import serializers
from client.serializers import ClientSerializer
from appartement.serializers import AppartementSerializers
from tools.serializers import RelationModelSerializer
from client.models import Client
from appartement.models import Appartement
from django.db import transaction
from .models import *
from rest_framework.utils.model_meta import get_field_info
#pip install xmtodict later on /'''

class AccesoireloyerSerializers(RelationModelSerializer):
    """ Serializers for model Accesoireloyer"""
    class Meta:
        model = Accesoireloyer
        fields = '__all__'


class ContratSerializers(serializers.ModelSerializer):
    accessoires = serializers.SerializerMethodField()
    client = ClientSerializer(read_only=True, )
    client_id = serializers.PrimaryKeyRelatedField(source='Client',
                                                         queryset=Client.objects.all(), write_only=True, )
    appartement = AppartementSerializers(read_only=True)
    appartement_id = serializers.PrimaryKeyRelatedField(source='Appartement',
                                                   queryset=Appartement.objects.all(), write_only=True, )
    class Meta:
        model = Contrat
        fields =('id', 'reference_bail', 'date_signature', 'date_effet', 'periodicite', 'duree',
                 'montant_bail', 'statut', 'observation', 'tacite_reconduction',
                 'client', 'client_id', 'appartement', 'appartement_id', 'accessoires' )

    def get_accessoires(self, contrat):
        accessoires = ContratAccessoiresloyer.objects.filter(
            contrat=contrat.id,
        )
        return ContratAccessoiresloyerSerializers(
            accessoires,
            context=self.context,
            many=True,
        ).data

    @transaction.atomic
    def create(self, validated_data):
        client_instance = validated_data.pop('Client', None)
        appartement_instance = validated_data.pop('Appartement', None)
        contrat = Contrat.objects.create(client=client_instance, appartement=appartement_instance, **validated_data)
        if "accessoires" in self.initial_data:
            accessoires = self.initial_data.get("accessoires")
            for accessoire in accessoires:
                accessoire_instance = Accesoireloyer.objects.get(pk=accessoire.pop("accessoire_id", None))
                print(accessoire)
                accessoire.pop('contrat', None)
                ContratAccessoiresloyer(contrat_id=contrat.id, accesoireloyer_id=accessoire_instance.id, **accessoire).save()
        contrat.save()
        return contrat

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


class ContratAccessoiresloyerSerializers(serializers.ModelSerializer):
    """
    Structure Serializers
    """
    accesoireloyer = AccesoireloyerSerializers(read_only=True)
    accesoireloyer_id = serializers.PrimaryKeyRelatedField(source='Accesoireloyer',
                                                           queryset=Accesoireloyer.objects.all(), write_only=True, )
    #contrat = ContratSerializers(read_only=True)
    #contrat_id = serializers.PrimaryKeyRelatedField(source='Contrat', queryset=Contrat.objects.all(),)
    class Meta:
        model = ContratAccessoiresloyer
        fields = ('contrat', 'accesoireloyer', 'accesoireloyer_id', 'montant', 'devise',
                  'statut', 'devise', 'description')
