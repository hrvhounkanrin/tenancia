# -*- coding: UTF-8 -*-
import logging

from appartement.serializers import ( AppartementSerializers, StructureAppartmentSerializers, ComposantAppartmentSerializers,)
from appartement.models import (Appartement, ComposantAppartement, StructureAppartement, )
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)

class AppartementViewSet(ActionAPIView):
    def get_appartment(self, request, params ={} , *args, **kwargs):
        """  Get all  appartements """
        get_all_appartment = Appartement.objects.all()
        serialized_appartment = AppartementSerializers(get_all_appartment, many=True).data
        return {"success": True, "appartements": serialized_appartment}
    get_appartment.__doc__ = "  Get all  appartements "

    def get_building_appartment(self, request, params={}, *args, **kwargs):
        pass

    def create_appartment(self, request, params={}, *args, **kwargs):
        """
         Create appartement
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('appartement', None), list):
            appartements = request.data.pop('appartement')
            appart_objects = []
            for appart in appartements:
                serializer = AppartementSerializers(data=appart, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                appart_objects.append(serializer)
            saved_appartements = [model.save() for model in appart_objects]
            serialized_proprio = AppartementSerializers(saved_appartements, many=True, context=serializer_context)
            return {"success": True, "appartement": serialized_proprio.data}

        #print(request.data.pop('user'))
        serializer = AppartementSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "appartement": serializer.data}

    def update_appartement(self, request, params={}, *args, **kwargs):
        """
         Update appartement
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('appartement', None), list):
            appartements = request.data.pop('appartement')
            for appart in appartements:
                instance = Appartement.objects.get(pk=params.get('id', None))
                serializer = AppartementSerializers(instance, data=appart, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return {"success": True, "appartement": serializer.data}

        instance = Appartement.objects.get(pk=params.get('id', None))
        serializer = AppartementSerializers(instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "appartement": serializer.data}


class ComposantAppartementViewSet(ActionAPIView):

    def get_component(self, request, params ={} , *args, **kwargs):
        """  Get all avavaible appartement component whatever the language"""
        serializer_context = {
            'request': request,
        }

        if 'id' in params:
            queryset = ComposantAppartement.objects.filter(id__in=params['id'].split(","))
            serializer = ComposantAppartmentSerializers(queryset, context=serializer_context, many=True)
            logger.debug('**retrieving ComposantAppartement **')
            return serializer.data

        queryset = ComposantAppartement.objects.all()
        serializer = ComposantAppartmentSerializers(queryset, many=True)
        return {"success": True, "composantAppartements": serializer.data}
        get_component.__doc__ =  "The simple way to get the list of all the appartment component using the APIActionViewSet"

    def create_component(self, request, params={}, *args, **kwargs):
        """  Create an appartment component, it take a single component or a list of components"""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('composant_appartement', None), list):
            composants = request.data.pop('composant_appartement')
            aappartment_component_objects = []
            for composant in composants:
                serializer = ComposantAppartmentSerializers(data=composant, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                aappartment_component_objects.append(serializer)
            saved_components = [model.save() for model in aappartment_component_objects]
            serialized_composants = ComposantAppartmentSerializers(saved_components, context=serializer_context, many=True)
            return {"success": True, "composant_apart": serialized_composants.data}

        serializer = ComposantAppartmentSerializers(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "composant_apart": serializer.data}

    def update_component(self, request, params={}, *args, **kwargs):
        """
         Update Component
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('composant_appartement', None), list):
            components = request.data.pop('composant_appartement')
            component_objects = []
            for component in components:
                instance = ComposantAppartement.objects.get(pk=params.get('id', None))
                serializer = ComposantAppartmentSerializers(instance, data=component, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                component_objects.append(serializer)
            saved_components = [model.save() for model in component_objects]
            serializer = ComposantAppartmentSerializers(saved_components, many=True, context=serializer_context)
            return {"success": True, "composant_apart": serializer.data}

        instance = ComposantAppartement.objects.get(pk=params.get('id', None))
        serializer = ComposantAppartmentSerializers(instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "composant_apart": serializer.data}


class StructureAppartmentViewSet(ActionAPIView):
    def get_structure(self, request, params ={} , *args, **kwargs):
        """  Get all  structure """

        get_all_structure = StructureAppartement.objects.all()
        serialized_structure = StructureAppartmentSerializers(get_all_structure, many=True).data
        return {"success": True, "structures": serialized_structure}
        get_structure.__doc__ = "  Get all  structure "