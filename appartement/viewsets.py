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

    def create(self, request, *args, **kwargs):
        """
        Overrides the create method in order to save
        StructureAppartement objects if it exists in
        request.data.
        """
        structures_data = request.data.pop('structures', False)
        print(structures_data)
        serializer = AppartementSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        """Saving structureAppartement"""
        if structures_data:
            for structure in structures_data:
                structure_appartement_serializer = StructureAppartmentSerializers(data=structure)
                structure_appartement_serializer.is_valid(raise_exception=True)
                structure_appartement_serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ComposantAppartementViewSet(viewsets.ModelViewSet):
    queryset = ComposantAppartement.objects.all()
    serializer_class = ComposantAppartmentSerializers

class StructureAppartementViewset(viewsets.ModelViewSet):
    queryset = StructureAppartement.objects.all()
    serializer_class = StructureAppartmentSerializers