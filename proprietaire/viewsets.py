# -*- coding: UTF-8 -*-
"""Proprietaire app viewsets."""
from django.shortcuts import get_object_or_404
import logging
from .serializers import ProprietaireSerializers
from proprietaire.models import Proprietaire
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)


class ProprietairAction(ActionAPIView):
    """Get proprietaire action view."""

    def get_proprio(self, request, params={}, detail=None, *args, **kwargs):
        """
        Get the proprieatire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return: List proprietaire
        """
        serializer_context = {
            'request': request,
        }
        if 'id' in params:
            queryset = Proprietaire.objects.filter(
                id__in=params['id'].split(','),
                created_by=self.request.user)
            serializer = ProprietaireSerializers(
                queryset, context=serializer_context, many=True)
            logger.debug('**retrieving prorpio **')
            return serializer.data
        queryset = Proprietaire.objects.filter(
            created_by=self.request.user)
        serializer = ProprietaireSerializers(
            queryset, context=serializer_context, many=True)
        return {'success': True, 'payload': serializer.data}

    def create_proprio(self, request, params={}, *args, **kwargs):
        """
        Create proprio based on existing user.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return: Proprietaire
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('proprietaire', None), list):
            proprietaires = request.data.pop('proprietaire')
            proprietaire_objects = []
            for proprio in proprietaires:
                proprio['user_id'] = request.user.id
                serializer = ProprietaireSerializers(
                    data=proprio, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                proprietaire_objects.append(serializer)
            saved_proprio = \
                [model.save(created_by=request.user)
                 for model in proprietaire_objects]
            serialized_proprio = ProprietaireSerializers(
                saved_proprio, many=True, context=serializer_context)
            return {'success': True, 'proprietaire': serialized_proprio.data}
        request.data['user_id'] = request.user.id
        serializer = ProprietaireSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {'success': True, 'proprietaire': serializer.data}

    def update_proprio(self, request, params={}, *args, **kwargs):
        """
        Update proprietaire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('proprietaire', None), list):
            proprietaires = request.data.pop('proprietaire')
            proprietaire_objects = []
            for proprio in proprietaires:
                instance = get_object_or_404(Proprietaire.objects.filter(
                    created_by=self.request.user), pk=params.get('id', None))
                serializer = ProprietaireSerializers(
                    instance, data=proprio, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                proprietaire_objects.append(serializer)
            saved_proprio = \
                [model.save(modified_by=request.user)
                 for model in proprietaire_objects]
            serializer = ProprietaireSerializers(
                saved_proprio, many=True, context=serializer_context)
            return {'success': True, 'proprietaire': serializer.data}
        instance = get_object_or_404(Proprietaire, pk=params.get('id', None))
        serializer = ProprietaireSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        return {'success': True, 'proprietaire': serializer.data}
