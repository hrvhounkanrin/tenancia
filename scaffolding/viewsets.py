# -*- coding: UTF-8 -*-
"""Scaffolding app viewsets."""
import logging

from .models import Appartement
from .models import Immeuble
from .serialisers import AppartementSerializers
from .serialisers import ImmeubleSerializers
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)


class SampleImmeubleViewSet(ActionAPIView):
    """Sample immeuble viewset action."""

    def get_immeuble(self, request, params={}, *args, **kwargs):
        """Get immeuble."""
        serializer_context = {
            'request': request,
        }
        if 'id' in params:
            queryset = Immeuble.objects.filter(
                id__in=params['id'].split(','))
            serializer = ImmeubleSerializers(
                queryset, context=serializer_context, many=True)
            logger.debug('**retrieving immeubles **')
            return {'success': True, 'immeubles': serializer.data}
        get_all_immeuble = Immeuble.objects.all()
        serialized_immeuble = ImmeubleSerializers(
            get_all_immeuble, context=serializer_context, many=True)
        return {'success': True, 'immeubles': serialized_immeuble.data}

    def create_immeuble(self, request, params={}, *args, **kwargs):
        """Create immeuble."""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('immeuble', None), list):
            immeubles = request.data.pop('immeuble')
            immeuble_objects = []
            for immeuble in immeubles:
                serializer = ImmeubleSerializers(
                    data=immeuble, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeuble = [model.save() for model in immeuble_objects]
            serialized_proprio = ImmeubleSerializers(
                saved_immeuble, context=serializer_context, many=True)
            return {'success': True, 'immeuble': serialized_proprio.data}
        serializer = ImmeubleSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'immeuble': serializer.data}

    def update_immeuble(self, request, params={}, *args, **kwargs):
        """
        Update Immeuble.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('immeuble', None), list):
            immeubles = request.data.pop('immeuble')
            immeuble_objects = []
            for immeuble in immeubles:
                instance = Immeuble.objects.get(
                    pk=params.get('id', None))
                serializer = ImmeubleSerializers(
                    instance, data=immeuble, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeubles = [model.save() for model in immeuble_objects]
            serializer = ImmeubleSerializers(
                saved_immeubles, many=True, context=serializer_context)
            return {'success': True, 'immeuble': serializer.data}
        instance = Immeuble.objects.get(
            pk=params.get('id', None))
        serializer = ImmeubleSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'immeuble': serializer.data}


class SampleAppartementViewSet(ActionAPIView):
    """Appartement model."""

    def get_appartment(self, request, params={}, *args, **kwargs):
        """Get  appartements."""
        get_all_appartment = Appartement.objects.all()
        serialized_appartment = AppartementSerializers(
            get_all_appartment, many=True).data
        return {'success': True, 'appartements': serialized_appartment}

    def create_appartment(self, request, params={}, *args, **kwargs):
        """
        Create appartement.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return: Appartement
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('appartement', None), list):
            appartements = request.data.pop('appartement')
            appart_objects = []
            for appart in appartements:
                serializer = AppartementSerializers(
                    data=appart, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                appart_objects.append(serializer)
            saved_appartements = [model.save() for model in appart_objects]
            serialized_appart = AppartementSerializers(
                saved_appartements, many=True, context=serializer_context)
            return {'success': True, 'appartement': serialized_appart.data}
        serializer = AppartementSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'appartement': serializer.data}

    def update_appartement(self, request, params={}, *args, **kwargs):
        """
        Update appartement.

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
                instance = Appartement.objects.get(
                    pk=params.get('id', None))
                serializer = AppartementSerializers(
                    instance, data=appart, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return {'success': True, 'appartement': serializer.data}
        instance = Appartement.objects.get(pk=params.get('id', None))
        serializer = AppartementSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'appartement': serializer.data}
