"""RealEstate app viewsets."""
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect
from tools.viewsets import ActionAPIView
from .models import Mandat, RealEstate, RealEstateUsers
from .serializers import MandatSerializer, SocieteSerializer

logger = logging.getLogger(__name__)


class SocieteViewSetAction(ActionAPIView):
    """RealEstate action viewset."""

    def get_mandataire(self, request, params={}, *args, **kwargs):
        """
        Get  mandatire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return: mandatire
        """
        serializer_context = {"request": request}
        if "id" in params:
            queryset = RealEstate.objects.filter(id__in=params["id"].split(","))
            serializer = SocieteSerializer(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving mandataire **")
            return serializer.data

        queryset = RealEstate.objects.all()
        serializer = SocieteSerializer(queryset, context=serializer_context, many=True)
        return {"success": True, "payload": serializer.data}

    def create_mandataire(self, request, params={}, *args, **kwargs):
        """
        Create mandataire based on connected user.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {"request": request}
        current_user = get_user_model().objects.get(pk=request.user.id)
        if isinstance(request.data.get("mandataire", None), list):
            mandataires = request.data.pop("mandataire")
            mandataire_objects = []
            mandataire_objects = []
            for mandataire in mandataires:
                serializer = SocieteSerializer(
                    data=mandataire, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                mandataire_objects.append(serializer)
            saved_mandataire = [model.save() for model in mandataire_objects]
            [
                RealEstateUsers(societe=sc, user=current_user, profil="MASTER").save()
                for sc in saved_mandataire
            ]
            serialized_mandataire = SocieteSerializer(
                saved_mandataire, many=True, context=serializer_context
            )
            return {'success"': True, "payload": serialized_mandataire.data}
        serializer = SocieteSerializer(data=request.data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = ''.join([settings.BASE_API_URL, 'profile_action/get_profile'])
        return redirect(url, *args, permanent=False, **kwargs)
        #return {"success": True, "payload": serializer.data}

    def update_mandataire(self, request, params={}, *args, **kwargs):
        """
        Update mandataire.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {"request": request}
        if isinstance(request.data.get("societe", None), list):
            mandataires = request.data.pop("societe")
            mandataire_objects = []
            for mandataire in mandataires:
                instance = RealEstate.objects.get(pk=params.get("id", None))
                serializer = SocieteSerializer(
                    instance, data=mandataire, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                mandataire_objects.append(serializer)
            saved_mandataire = [model.save() for model in mandataire_objects]
            serializer = SocieteSerializer(
                saved_mandataire, many=True, context=serializer_context
            )
            return {"success": True, "payload": serializer.data}
        instance = get_object_or_404(RealEstate, pk=params.get("id", None))
        serializer = SocieteSerializer(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}


class MandatViewSetAction(ActionAPIView):
    """Get mandat."""

    def get_mandat(self, request, params={}, *args, **kwargs):
        """
        Get  mandat.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:Mandat
        """
        serializer_context = {"request": request}
        if "id" in params:
            queryset = Mandat.objects.filter(id__in=params["id"].split(","))
            serializer = MandatSerializer(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving mandats **")
            return serializer.data
        queryset = Mandat.objects.all()
        serializer = MandatSerializer(queryset, context=serializer_context, many=True)
        return {"success": True, "payload": serializer.data}

    def create_mandat(self, request, params={}, *args, **kwargs):
        """
        Create mandat based on connected user.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return: mandat
        """
        serializer_context = {"request": request}
        if isinstance(request.data.get("mandat", None), list):
            mandats = request.data.pop("mandat")
            mandat_objects = []
            for mandat in mandats:
                serializer = MandatSerializer(data=mandat, context=serializer_context)
                serializer.is_valid(raise_exception=True)
                mandat_objects.append(serializer)
            saved_mandat = [model.save() for model in mandat_objects]
            serialized_mandat = MandatSerializer(
                saved_mandat, many=True, context=serializer_context
            )
            return {"success": True, "payload": serialized_mandat.data}
        serializer = MandatSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}

    def update_mandat(self, request, params={}, *args, **kwargs):
        """
        Update mandat.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {"request": request}
        if isinstance(request.data.get("mandat", None), list):
            mandats = request.data.pop("mandat")
            mandat_objects = []
            for mandat in mandats:
                instance = Mandat.objects.get(pk=params.get("id", None))
                serializer = MandatSerializer(
                    instance, data=mandat, context=serializer_context
                )
                serializer.is_valid(raise_exception=True)
                mandat_objects.append(serializer)
            saved_mandat = [model.save() for model in mandat_objects]
            serializer = MandatSerializer(
                saved_mandat, many=True, context=serializer_context
            )
            return {"success": True, "payload": serializer.data}

        instance = Mandat.objects.get(pk=params.get("id", None))
        serializer = MandatSerializer(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "payload": serializer.data}
