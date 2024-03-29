"""Client app Actions Viewset."""
import logging
from django.conf import settings
from rest_framework import permissions
from django.shortcuts import get_object_or_404, redirect
from client.models import Client
from tools.viewsets import ActionAPIView
from .serializers import ClientSerializer
from customuser.permissions import IsLessor, IsTenant
from django.db.models import Q
logger = logging.getLogger(__name__)


class ClientAction(ActionAPIView):
    """Client action viewset."""

    def __init__(self):
        self.permission_classes = {
        "get_client":  [permissions.IsAuthenticated, IsLessor],
        "create_client": [permissions.IsAuthenticated],
        "update_client": [permissions.IsAuthenticated, IsTenant],
        "retrieve_client": [IsLessor]
        }

    def get_client(self, request, params={}, *args, **kwargs):
        print('ClientAction get_client')
        """
         Get all the client without a specif params for now.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        if "id" in params:
            queryset = Client.objects.filter(
                id__in=params["id"].split(","), created_by=request.user
            )
            serializer = ClientSerializer(
                queryset, context={"request": request}, many=True
            )
            logger.debug("**retrieving client **")
            return serializer.data

        queryset = Client.objects.filter(user_id=request.user)
        serializer = ClientSerializer(queryset, context={"request": request}, many=True)
        return {"success": True, "payload": serializer.data}

    def create_client(self, request, params={}, *args, **kwargs):
        """
        Create client based on existing user.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        """
        if isinstance(request.data.get('client', None), list):
            clients = request.data.pop('client')
            client_objects = []
            for client in clients:
                serializer = ClientSerializer(
                    data=client, context={'request': request})
                serializer.is_valid(raise_exception=True)
                client_objects.append(serializer)

            saved_clients = [model.save(user_id=request.user.id) for model in client_objects]
            serrialized_client = ClientSerializer(
                saved_clients, many=True, context={'request': request})
            return {'success': True, 'client': serrialized_client.data}
        """
        request.data["user_id"] = request.user.id
        serializer = ClientSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = ''.join([settings.BASE_API_URL, 'profile_action/get_profile'])
        return redirect(url, *args, permanent=False, **kwargs)
        # return {"success": True, "payload": serializer.data}

    def update_client(self, request, params={}, *args, **kwargs):
        """
         Update Client.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        serializer_context = {
            "request": request,
        }
        request.data["user_id"] = request.user.id
        instance = get_object_or_404(Client, pk=params.get("id", None))
        serializer = ClientSerializer(
            instance, data=request.data, context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        url = ''.join([settings.BASE_API_URL, 'profile_action/get_profile'])
        return redirect(url, *args, permanent=False, **kwargs)
        # return {"success": True, "payload": serializer.data}

    def retrieve_client(self, request, params={}, *args, **kwargs):
        """
         Get all the client without a specif params for now.

        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        email = params.get('q', None)
        if email is None:
            return {"success": True, "payload": []}
        queryset = Client.objects.filter(user__email__startswith=email)
        serializer = ClientSerializer(queryset, context={"request": request}, many=True)
        return {"success": True, "payload": serializer.data}