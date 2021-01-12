# -*- coding: UTF-8 -*-
"""Contrat Actions viewsets."""
import logging
from django.shortcuts import get_object_or_404
from .models import Accesoireloyer
from .models import Contrat
from .models import ContratAccessoiresloyer
from .serializers import AccesoireloyerSerializers
from .serializers import ContratAccessoiresloyerSerializers
from .serializers import ContratSerializers
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)


class AccessoireloyerAction(ActionAPIView):
    """ContratAccessoireloyer actions viewet."""

    def get_accessoire(self, request, params={}, *args, **kwargs):
        """Get acessoires loyer."""
        serializer_context = {
            'request': request,
        }
        queryset = Accesoireloyer.objects.all()
        serializer = AccesoireloyerSerializers(queryset, many=True,
                                               context=serializer_context)
        return {'success': True, 'accessoireloyer': serializer.data}

    def create_accessoire(self, request, params={}, *args, **kwargs):
        """Create accessoireloyer."""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('accessoire', None), list):
            accesoires = request.data.pop('accessoire')
            acc___objects = []
            for acc in accesoires:
                serializer = AccesoireloyerSerializers(
                    data=acc, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                acc___objects.append(serializer)
            saved_acc = [model.save() for model in acc___objects]
            serialized_acc = AccesoireloyerSerializers(
                saved_acc, context=serializer_context, many=True)
            return {'success': True, 'accessoireloyer': serialized_acc.data}
        serializer = AccesoireloyerSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'accessoire': serializer.data}

    def update_accessoire(self, request, params={}, *args, **kwargs):
        """
        Update Accessoire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('accessoire', None), list):
            accessoires = request.data.pop('accessoire')
            acc_objects = []
            for acc in accessoires:
                instance = Accesoireloyer.objects.get(
                    pk=params.get('id', None))
                serializer = AccesoireloyerSerializers(
                    instance, data=acc, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                acc_objects.append(serializer)
            saved_components = [model.save() for model in acc_objects]
            serializer = AccesoireloyerSerializers(
                saved_components, many=True, context=serializer_context)
            return {'success': True, 'accessoireloyer': serializer.data}
        instance = get_object_or_404(Accesoireloyer,
                                     pk=params.get('id', None))
        serializer = AccesoireloyerSerializers(
            instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'accessoire': serializer.data}


class ContratAccessoiresloyerAction(ActionAPIView):
    """ContratAccessoireloyer Action Viewset."""

    queryset = ContratAccessoiresloyer.objects.all()
    serializer_class = ContratAccessoiresloyerSerializers


class ContratAction(ActionAPIView):
    """Contrat Action viewset."""

    def get_contrat(self, request, params={}, *args, **kwargs):
        """Get contrat."""
        if 'id' in params:
            queryset = Contrat.objects.filter(
                id__in=params['id'].split(','))
            serializer = ContratSerializers(
                queryset, context={'request': request}, many=True)
            logger.debug('**retrieving Contrat **')
            return {'success': True, 'contrat': serializer.data}
        queryset = Contrat.objects.all()
        serializer = ContratSerializers(
            queryset, many=True, context={'request': request})
        return {'success': True, 'contrat': serializer.data}

    def create_contrat(self, request, params={}, *args, **kwargs):
        """Create contract."""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('contrat', None), list):
            contrats = request.data.pop('contrat')
            contrat_objects = []
            for contrat in contrats:
                serializer = ContratSerializers(
                    data=contrat, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                contrat_objects.append(serializer)
            saved_contrat = [model.save() for model in contrat_objects]
            serialized_contrat = ContratSerializers(
                saved_contrat, context=serializer_context, many=True)
            return {'success': True, 'contrat': serialized_contrat.data}
        serializer = ContratSerializers(
            data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'contrat': serializer.data}

    def update_contrat(self, request, params={}, *args, **kwargs):
        """Update contract."""
        serializer_context = {
            'request': request,
        }
        if isinstance(request.data.get('contrat', None), list):
            contrats = request.data.pop('contrat')
            contrat_objects = []
            for contrat in contrats:
                serializer = ContratSerializers(
                    data=contrat, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                contrat_objects.append(serializer)
            saved_contrat = [model.save() for model in contrat_objects]
            serialized_contrat = ContratSerializers(
                saved_contrat, context=serializer_context, many=True)
            return {'success': True, 'contrat': serialized_contrat.data}
        serializer = ContratSerializers(data=request.data,
                                        context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {'success': True, 'contrat': serializer.data}
