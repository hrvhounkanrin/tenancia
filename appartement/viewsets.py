# -*- coding: UTF-8 -*-
"""Housing app Action viewset."""
import logging
from django.shortcuts import get_object_or_404
from appartement.models import Appartement
from appartement.models import ComposantAppartement
from appartement.models import StructureAppartement
from appartement.serializers import AppartementSerializers
from appartement.serializers import ComposantAppartmentSerializers
from appartement.serializers import StructureAppartmentSerializers
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)


class AppartementViewSet(ActionAPIView):
    """Housing Viewset."""

    def get_logement(self, request, params={}, *args, **kwargs):
        """Get housing."""
        serializer_context = {
            'request': request,
        }
        if len(params) == 0:
            queryset = Appartement.objects.filter(created_by=self.request.user)
        if 'id' in params:
            queryset = Appartement.objects.filter(
                id__in=params['id'].split(','), created_by=self.request.user)
        if 'immeuble_id' in params:
            queryset = Appartement.objects.filter(
                immeuble_id=params['immeuble_id'], created_by=self.request.user)
        serializer = AppartementSerializers(
            queryset, context=serializer_context, many=True)
        logger.debug('**retrieving housing **')
        return {'success': True, 'logement': serializer.data}

    def create_logement(self, request, params={}, *args, **kwargs):
        """
         Create appartement.

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
                serializer = AppartementSerializers(
                    data=appart, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                appart_objects.append(serializer)
            saved_appartements = \
                [model.save(created_by=request.user)
                 for model in appart_objects]
            serialized_proprio = AppartementSerializers(
                saved_appartements, many=True, context=serializer_context)
            return {'success': True, 'appartement': serialized_proprio.data}
        serializer = AppartementSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {'success': True, 'logement': serializer.data}

    def update_logement(self, request, params={}, *args, **kwargs):
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
                serializer.save(modified_by=request.user)
                return {'success': True, 'logement': serializer.data}
        instance = get_object_or_404(Appartement, pk=params.get('id', None))
        serializer = AppartementSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        return {'success': True, 'logement': serializer.data}


class ComposantAppartementViewSet(ActionAPIView):
    """Housing dependency Action Viewset."""

    def get_dependency(self, request, params={}, *args, **kwargs):
        """Get all housing dependencies."""
        serializer_context = {
            'request': request,
        }

        if 'id' in params:
            queryset = ComposantAppartement.objects.filter(
                id__in=params['id'].split(','))
            serializer = ComposantAppartmentSerializers(
                queryset, context=serializer_context, many=True)
            logger.debug('**retrieving housing dependencies **')
            return serializer.data

        queryset = ComposantAppartement.objects.all()
        serializer = ComposantAppartmentSerializers(queryset, many=True)
        return {'success': True, 'dependency': serializer.data}

    def create_dependency(self, request, params={}, *args, **kwargs):
        """Create housing dependency."""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('housing_dependency', None), list):
            dependencies = request.data.pop('housing_dependency')
            housing_dependency_objects = []
            for dependency in dependencies:
                serializer = ComposantAppartmentSerializers(
                    data=dependency, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                housing_dependency_objects.append(serializer)
            saved_dependencies = [model.save()
                                  for model in housing_dependency_objects]
            serialized_dependencies = ComposantAppartmentSerializers(
                saved_dependencies, context=serializer_context,
                many=True)
            return {'success': True,
                    'dependency': serialized_dependencies.data}
        serializer = ComposantAppartmentSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'dependency': serializer.data}

    def update_dependency(self, request, params={}, *args, **kwargs):
        """
         Update housing dependency.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('housing_dependency', None), list):
            dependencies = request.data.pop('housing_dependency')
            dependency_objects = []
            for dependency in dependencies:
                instance = ComposantAppartement.objects.get(
                    pk=params.get('id', None))
                serializer = ComposantAppartmentSerializers(
                    instance, data=dependency, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                dependency_objects.append(serializer)
            saved_dependencies = [model.save() for model in dependency_objects]
            serializer = ComposantAppartmentSerializers(
                saved_dependencies, many=True, context=serializer_context)
            return {'success': True, 'dependance': serializer.data}
        instance = get_object_or_404(ComposantAppartement,
                                     pk=params.get('id', None))
        serializer = ComposantAppartmentSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'dependance': serializer.data}


class StructureAppartmentViewSet(ActionAPIView):
    """StructureAppartement Actions viewset."""

    def get_structure(self, request, params={}, *args, **kwargs):
        """Get all  structure."""
        get_all_structure = StructureAppartement.objects.all()
        serialized_structure = StructureAppartmentSerializers(
            get_all_structure, many=True).data
        return {'success': True, 'structures': serialized_structure}
