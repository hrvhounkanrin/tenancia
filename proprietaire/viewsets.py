# -*- coding: UTF-8 -*-
import logging
from .serializers import ProprietaireSerializers
from proprietaire.models import  *
from tools.viewsets import ActionAPIView
logger = logging.getLogger(__name__)

class ProprietairAction(ActionAPIView):
    ' Get all proprietaire'
    def get_proprio(self, request, params={}, *args, **kwargs):
        """
         Get all the proprieatire without a specif params for now
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
            queryset = Proprietaire.objects.filter(id__in=params['id'].split(","))
            serializer = ProprietaireSerializers(queryset, context=serializer_context, many=True)
            logger.debug('**retrieving prorpio **')
            return serializer.data

        queryset = Proprietaire.objects.all()
        serializer = ProprietaireSerializers(queryset, context=serializer_context, many=True)
        return {"success": True, "payload": serializer.data}

    def create_proprio(self, request, params={}, *args, **kwargs):
        """
         Create proprio based on existing user
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
                serializer = ProprietaireSerializers(data=proprio, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                proprietaire_objects.append(serializer)
            saved_proprio = [model.save() for model in proprietaire_objects]
            serialized_proprio = ProprietaireSerializers(saved_proprio, many=True, context=serializer_context)
            return {"success": True, "proprietaire": serialized_proprio.data}

        #print(request.data.pop('user'))
        serializer = ProprietaireSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "proprietaire": serializer.data}


    def update_proprio(self, request, params={}, *args, **kwargs):
        """
         Update proprio
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
                instance = Proprietaire.objects.get(pk=params.get('id', None))
                serializer = ProprietaireSerializers(instance, data=proprio, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                proprietaire_objects.append(serializer)
            saved_proprio = [model.save() for model in proprietaire_objects]
            serializer = ProprietaireSerializers(saved_proprio, many=True, context=serializer_context)
            return {"success": True, "proprietaire": serializer.data}

        instance = Proprietaire.objects.get(pk=params.get('id', None))
        serializer = ProprietaireSerializers(instance, data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "proprietaire": serializer.data}
