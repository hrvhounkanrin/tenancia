# -*- coding: UTF-8 -*-
import logging
from .serializers import *
from .models import  *
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)

class SocieteViewSetAction(ActionAPIView):
    ' Get all mandataires'
    def get_mandataire(self, request, params={}, *args, **kwargs):
        """
         Get all manddatire
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """

        serializer_context = {
            'request': request,
        }
        if 'id' in params:
            queryset = Societe.objects.filter(id__in=params['id'].split(","))
            serializer = SocieteSerializer(queryset, context=serializer_context, many=True)
            logger.debug('**retrieving mandataire **')
            return serializer.data

        queryset = Societe.objects.all()
        serializer = SocieteSerializer(queryset, context=serializer_context, many=True)
        return {"success": True, "payload": serializer.data}

    def create_mandataire(self, request, params={}, *args, **kwargs):
        """
         Create mandataire based on connected user
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('mandataire', None), list):
            print("Liste de mandataire")
            mandataires = request.data.pop('mandataire')
            mandataire_objects = []
            for mandataire in mandataires:
                serializer = SocieteSerializer(data=mandataire, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                mandataire_objects.append(serializer)
            saved_mandataire = [model.save() for model in mandataire_objects]
            serialized_mandataire = SocieteSerializer(saved_mandataire, many=True, context=serializer_context)
            return {"success": True, "societe": serialized_mandataire.data}

        #print(request.data.pop('user'))
        serializer = SocieteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "societe": serializer.data}


    def update_mandataire(self, request, params={}, *args, **kwargs):
        """
         Update mandataire
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('societe', None), list):
            mandataires = request.data.pop('societe')
            mandataire_objects = []
            for mandataire in mandataires:
                instance = Societe.objects.get(pk=params.get('id', None))
                serializer = SocieteSerializer(instance, data=mandataire, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                mandataire_objects.append(serializer)
            saved_mandataire = [model.save() for model in mandataire_objects]
            serializer = SocieteSerializer(saved_mandataire, many=True, context=serializer_context)
            return {"success": True, "societe": serializer.data}

        instance = Societe.objects.get(pk=params.get('id', None))
        serializer = SocieteSerializer(instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "societe": serializer.data}
    

class MandatViewSetAction(ActionAPIView):
    ' Get all mandat'
    def get_mandat(self, request, params={}, *args, **kwargs):
        """
         Get all mandat
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """

        serializer_context = {
            'request': request,
        }
        if 'id' in params:
            queryset = Mandat.objects.filter(id__in=params['id'].split(","))
            serializer = MandatSerializer(queryset, context=serializer_context, many=True)
            logger.debug('**retrieving mandats **')
            return serializer.data

        queryset = Mandat.objects.all()
        serializer = MandatSerializer(queryset, context=serializer_context, many=True)
        return {"success": True, "payload": serializer.data}

    def create_mandat(self, request, params={}, *args, **kwargs):
        """
         Create mandat based on connected user
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('mandat', None), list):
            print("Liste de mandat")
            mandats = request.data.pop('mandat')
            mandat_objects = []
            for mandat in mandats:
                serializer = MandatSerializer(data=mandat, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                mandat_objects.append(serializer)
            saved_mandat = [model.save() for model in mandat_objects]
            serialized_mandat = MandatSerializer(saved_mandat, many=True, context=serializer_context)
            return {"success": True, "mandat": serialized_mandat.data}

        #print(request.data.pop('user'))
        serializer = MandatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "mandat": serializer.data}


    def update_mandat(self, request, params={}, *args, **kwargs):
        """
         Update mandat
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('mandat', None), list):
            mandats = request.data.pop('mandat')
            mandat_objects = []
            for mandat in mandats:
                instance = Mandat.objects.get(pk=params.get('id', None))
                serializer = MandatSerializer(instance, data=mandataire, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                mandat_objects.append(serializer)
            saved_mandat = [model.save() for model in mandat_objects]
            serializer = MandatSerializer(saved_mandat, many=True, context=serializer_context)
            return {"success": True, "mandat": serializer.data}

        instance = Mandat.objects.get(pk=params.get('id', None))
        serializer = MandatSerializer(instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "mandat": serializer.data}

