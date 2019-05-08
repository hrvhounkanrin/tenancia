from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .serializers import ProprietaireSerializers
from proprietaire.models import  *
from tools.viewsets import  ActionAPIView


class ProprietairAction(ActionAPIView):
    ' Get all proprietaire'
    def get_proprio(self, request, params={}, *args, **kwargs):
        """
         Get all the proprieatire without a specif params for now
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        proprio_all = Proprietaire.objects.all()
        serialized_obj = ProprietaireSerializers(proprio_all, many=True).dat
        return {"success":True, "payload":serialized_obj}

class ProprietaireViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Proprietaire.objects.all()
    serializer_class = ProprietaireSerializers

    """
    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Immeuble.objects.all()
        else:
            connected_proprietaire=Proprietaire.objects.filter(user=self.request.user)
            queryset = Immeuble.objects.filter(proprietaire=connected_proprietaire)

        return queryset
    """
