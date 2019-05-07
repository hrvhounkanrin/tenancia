from rest_framework.permissions import IsAuthenticated

from .models import  Contrat
from .serializers import (AccesoireloyerSerializers, ContratAccessoiresloyerSerializers, ContratSerializers, )
from .models import (Accesoireloyer, ContratAccessoiresloyer, Contrat, )
from rest_framework.decorators import permission_classes
from rest_framework import  viewsets, permissions

class AccessoireloyerViewSet(viewsets.ModelViewSet):
    queryset = Accesoireloyer.objects.all()
    serializer_class = AccesoireloyerSerializers

class ContratAccessoiresloyerViewSet(viewsets.ModelViewSet):
    queryset = ContratAccessoiresloyer.objects.all()
    serializer_class = ContratAccessoiresloyerSerializers

class ContratViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Contrat.objects.all()
    serializer_class = ContratSerializers

    def get_queryset(self):
        #Queryset should be defined by user role(Client, Proprietaire, Staff, Admin)
        queryset = Contrat.objects.all()
        return queryset

