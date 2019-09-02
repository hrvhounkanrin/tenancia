from rest_framework import viewsets
from .serializers import BanqueSerializers
from .models import Banque


class BanqueViewSet(viewsets.ModelViewSet):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializers
