from rest_framework import viewsets, permissions
from mcore.models import Banque
from rest_framework.permissions import IsAuthenticated
from mcore.serializers import BanqueSerializer
from mcore.permissions import IsAdminOrReadOnly
class BanqueViewSet(viewsets.ModelViewSet):
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializer
    permission_classes = [IsAdminOrReadOnly,]

