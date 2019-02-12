from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from  proprietaire.models import Proprietaire
from .serializers import ImmeubleSerializers

from .models import Immeuble


class ImmeubleViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Immeuble.objects.all()
    serializer_class = ImmeubleSerializers

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Immeuble.objects.all()
        else:
            connected_proprietaire=Proprietaire.object.filter(user=self.request.user)
            queryset = Immeuble.objects.filter(proprietaire=connected_proprietaire)

        return queryset

