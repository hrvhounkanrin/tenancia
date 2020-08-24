# -*- coding: UTF-8 -*-
"""Customuser app viewsets."""
import logging

from proprietaire.serializers import ProprietaireSerializers
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from tools.viewsets import ActionAPIView
from proprietaire.models import Proprietaire
from client.models import Client
from client.serializers import ClientSerializer

logger = logging.getLogger(__name__)


class CustomUserAction(ActionAPIView):
    """Customuser actionview."""

    def get_profile(self, request, params={}, *args, **kwargs):
        """Get all user profile."""
        User = get_user_model()
        try:
            user = User.objects.get(pk=request.user.id)
            serializer = UserSerializer(user)
            proprietaire = Proprietaire.objects.filter(
                user__id=request.user.id
            ).first()
            lessor_serializer = ProprietaireSerializers(proprietaire)
            client = Client.objects.filter(user__id=request.user.id).first()
            client_serializer = ClientSerializer(client)
            profiles = {"user": serializer.data}
            if proprietaire is not None:
                profiles.update({"bailleur": lessor_serializer.data})
            if client is not None:
                profiles.update({"locataire": client_serializer.data})
            return {"success": True, "profiles": profiles}
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            serializer = UserSerializer(user)
            return {"success": True, "user": serializer}
        else:
            return {"success": False, "msg": "An error occured."}
