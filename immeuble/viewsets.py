# -*- coding: UTF-8 -*-
"""Immeuble action viewset."""
import logging
from django.shortcuts import get_object_or_404
from customuser.permissions import IsLessor
from .models import Immeuble
from .serializers import ImmeubleSerializers
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)


class ImmeubleAction(ActionAPIView):
    """Immeuble Action apiview."""

    permission_classes = [IsLessor, ]

    def get_immeuble(self, request, params={}, *args, **kwargs):
        """Get immeubles."""
        serializer_context = {
            'request': request,
        }
        if 'id' in params:
            queryset = Immeuble.objects.filter(
                id__in=params['id'].split(','),
                created_by=self.request.user)
            serializer = ImmeubleSerializers(
                queryset, context=serializer_context, many=True)
            logger.debug('**retrieving immeubles **')
            return {'success': True, 'immeubles': serializer.data}
        get_all_immeuble = Immeuble.objects.filter(
            created_by=self.request.user)
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
            saved_immeuble = [model.save(created_by=request.user)
                              for model in immeuble_objects]
            serialized_proprio = ImmeubleSerializers(
                saved_immeuble, context=serializer_context, many=True)
            return {'success': True, 'immeuble': serialized_proprio.data}
        serializer = ImmeubleSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
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
                instance = get_object_or_404(Immeuble.objects.filter(
                    created_by=self.request.user), pk=params.get('id', None))
                serializer = ImmeubleSerializers(
                    instance, data=immeuble, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeubles = [model.save() for model in immeuble_objects]
            serializer = ImmeubleSerializers(
                saved_immeubles, many=True, context=serializer_context)
            return {'success': True, 'immeuble': serializer.data}
        instance = get_object_or_404(Immeuble.objects.filter(
            created_by=self.request.user), pk=params.get('id', None))
        serializer = ImmeubleSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'immeuble': serializer.data}
