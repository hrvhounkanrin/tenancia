from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from appartement.serializers import (AppartementSerializers, ComposantAppartmentSerializers, StructureAppartmentSerializers,)
from appartement.models import (Appartement, ComposantAppartement, StructureAppartement, )
from rest_framework import views, viewsets, authentication, permissions, mixins, pagination
from  client.serializers import ClientSerializer
from django.http import HttpResponse

class AppartementViewSet(viewsets.ModelViewSet):
    queryset = Appartement.objects.all()
    serializer_class = AppartementSerializers



class ComposantAppartementViewSet(viewsets.ModelViewSet):
    queryset = ComposantAppartement.objects.all()
    serializer_class = ComposantAppartmentSerializers

class StructureAppartementViewset(viewsets.ModelViewSet):
    queryset = StructureAppartement.objects.all()
    serializer_class = StructureAppartmentSerializers