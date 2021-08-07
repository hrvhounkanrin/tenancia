"""Proprietaire app viewsets."""
import logging

from django.shortcuts import get_object_or_404
from django.conf import settings
from proprietaire.models import Proprietaire
from tools.viewsets import ActionAPIView
from django.contrib.sites.shortcuts import get_current_site
from .serializers import ProprietaireSerializers
from django.shortcuts import reverse, redirect
from django.http import HttpResponseRedirect
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
            "request": request,
        }
        if "id" in params:
            queryset = Proprietaire.objects.filter(
                id__in=params["id"].split(","), created_by=self.request.user
            )
            serializer = ProprietaireSerializers(
                queryset, context=serializer_context, many=True
            )
            logger.debug("**retrieving prorpio **")
            return serializer.data
        queryset = Proprietaire.objects.filter(created_by=self.request.user)
        serializer = ProprietaireSerializers(
            queryset, context=serializer_context, many=True
        )
        return {"success": True, "payload": serializer.data}

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
            "request": request,
        }
        serializer = ProprietaireSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=request.user)
        request.data["user_id"] = request.user.id
        url = ''.join([settings.BASE_API_URL, 'profile_action/get_profile'])
        return redirect(url, *args, permanent=False, **kwargs)
        # return {"success": True, "payload": serializer.data}

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
            "request": request,
        }
        instance = get_object_or_404(Proprietaire, pk=params.get("id", None))
        data = request.data
        data["user_id"] = request.user.id

        serializer = ProprietaireSerializers(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(modified_by=request.user)
        url = ''.join([settings.BASE_API_URL, 'profile_action/get_profile'])
        return redirect(url, *args, permanent=False, **kwargs)
        #return {"success": True, "payload": serializer.data}
