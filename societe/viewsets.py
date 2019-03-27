from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from  proprietaire.models import Proprietaire
from .serializers import SocieteSerializer

from .models import Societe


class SocieteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Societe.objects.all()
    serializer_class = SocieteSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Societe.objects.all()
        else:
            queryset = Societe.objects.all()

        return queryset

