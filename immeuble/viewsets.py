from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from  proprietaire.models import Proprietaire
from .serializers import ImmeubleSerializers
from tools.viewsets import ActionAPIView
from .models import Immeuble


class ImmeubleAction(ActionAPIView):
    def get_immeuble(self, request, params ={} , *args, **kwargs):
        """  Get immeuble regardless of proprietaire and societe """
        get_all_immeuble = Immeuble.objects.all()
        serialized_immeuble = ImmeubleSerializers(get_all_immeuble, many=True).data
        return {"success": True, "immeubles": serialized_immeuble}
    get_immeuble.__doc__ = "  Get immeuble regardless of proprietaire and societe"



    def create_immeuble(self, request, params={}, *args, **kwargs):
        """Create immeuble"""
        if isinstance(request.data.get('immeuble', None), list):
            immeubles = request.data.pop('immeuble')
            immeuble_objects = []
            for immeuble in immeubles:
                serializer = ImmeubleSerializers(data=immeuble)
                serializer.is_valid(raise_exception=True)
                immeuble_objects.append(serializer)
            saved_immeuble = [model.save() for model in immeuble_objects]
            serialized_proprio = ImmeubleSerializers(saved_immeuble, many=True)
            return {"success": True, "immeuble": serialized_proprio.data}

        #print(request.data.pop('user'))
        serializer = ImmeubleSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "immeuble": serializer.data}
