"""Immeuble action viewset."""
import logging
import requests
from django.utils.crypto import get_random_string
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from customuser.permissions import IsLessor, IsRealEstate
from tools.viewsets import ActionAPIView

from .models import AutoName, Immeuble
from .serializers import ClonerImmeubleSerializer, ImmeubleSerializers

logger = logging.getLogger(__name__)


class ImmeubleAction(ActionAPIView):
    """Immeuble Action apiview."""

    def __init__(self):
        self.permission_classes = {
            "get_immeuble": [IsLessor, IsRealEstate],
            "create_immeuble": [IsRealEstate],
            "update_immeuble": [IsLessor, IsRealEstate],
            "cloner_immeuble": [IsLessor, IsRealEstate],
            "reverse_geocoding": [IsAuthenticated, IsRealEstate],
        }

    def get_immeuble(self, request, params={}, *args, **kwargs):
        """Get immeubles."""
        serializer_context = {
            "request": request,
        }
        queryset = Immeuble.objects.filter(created_by=self.request.user)

        if "statut" in params:
            queryset = Immeuble.objects.filter(created_by=self.request.user)

        if "id" in params:
            queryset = Immeuble.objects.filter(
                id__in=params["id"].split(","), created_by=self.request.user
            )

        serializer = ImmeubleSerializers(
            queryset, context=serializer_context, many=True
        )
        logger.debug("**retrieving immeubles **")
        return {"success": True, "payload": serializer.data}



    def create_immeuble(self, request, params={}, *args, **kwargs):
        """Create immeuble."""
        serializer_context = {
            "request": request,
        }
        if isinstance(request.data.get("immeuble", None), list):
            immeubles = request.data.pop("immeuble")
            immeuble_objects = []
            for immeuble in immeubles:
                if not immeuble["intitule"]:
                    autoname = AutoName.objects.random()
                    immeuble["intitule"] = autoname.libelle
                serializer = ImmeubleSerializers(
                    data=immeuble, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeuble = [
                model.save(created_by=request.user) for model in immeuble_objects
            ]
            serialized_proprio = ImmeubleSerializers(
                saved_immeuble, context=serializer_context, many=True
            )
            return {"success": True, "payload": serialized_proprio.data}

        data = request.data
        if data.get('intitule', None) is None or data.get('intitule', None) == '':
            autoname = AutoName.objects.random()
            data["intitule"] = autoname.libelle
        if data.get('ref_immeuble', None) is None or data.get('ref_immeuble', None) == '':
            data['ref_immeuble'] = get_random_string(8).upper()
        serializer = ImmeubleSerializers(data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {"success": True, "payload": serializer.data}

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
            "request": request,
        }
        if isinstance(request.data.get("immeuble", None), list):
            immeubles = request.data.pop("immeuble")
            immeuble_objects = []
            for immeuble in immeubles:
                instance = get_object_or_404(
                    Immeuble.objects.filter(created_by=self.request.user),
                    pk=params.get("id", None),
                )
                serializer = ImmeubleSerializers(
                    instance, data=immeuble, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeubles = [model.save() for model in immeuble_objects]
            serializer = ImmeubleSerializers(
                saved_immeubles, many=True, context=serializer_context
            )
            return {"success": True, "payload": serializer.data}
        instance = get_object_or_404(
            Immeuble.objects.filter(created_by=self.request.user),
            pk=params.get("id", None),
        )
        data = request.data
        if data.get('intitule', None) is None or data.get('intitule', None) == '':
            autoname = AutoName.objects.random()
            data["intitule"] = autoname.libelle
        if data.get('ref_immeuble', None) is None or data.get('ref_immeuble', None) == '':
            data['ref_immeuble'] = get_random_string(8).upper()
        serializer = ImmeubleSerializers(
            instance, data=data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

    def cloner_immeuble(self, request, params={}, *args, **kwargs):
        """Multiplier un immeuble"""
        """
        Create immeuble.

       :param request:
       :param params:
       :param args:
       :param kwargs:
       :return:
       """
        serializer_context = {
            "request": request,
        }
        serializer = ClonerImmeubleSerializer(
            data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        return {"success": True, "payload": serializer.data}

    def reverse_geocoding(self, func_request, params={}, *args,**kwargs):
        api_key = 'AIzaSyBAkNKNluUXWFnVbxi-81lrdojzLx5MOyY'
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key={}".format(params.get('lat', None), params.get('lng', None), api_key)
        resp = requests.get(url=url)
        data = resp.json()
        return {"success": True, "payload": data}
