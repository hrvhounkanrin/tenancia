"""Banque Models."""
from rest_framework import viewsets

from .models import Banque
from .serializers import BanqueSerializers


class BanqueViewSet(viewsets.ModelViewSet):
    """Banque ViewSet."""

    queryset = Banque.objects.all()
    serializer_class = BanqueSerializers
