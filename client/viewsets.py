"""Client viewsets."""
from rest_framework import viewsets

from .models import Client
from client.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    """Client Viewset."""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
