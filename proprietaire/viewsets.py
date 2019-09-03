from rest_framework import viewsets
from .serializers import ProprietaireSerializers
from proprietaire.models import *
from tools.viewsets import ActionAPIView


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
        return {'success': True, 'payload': serialized_obj}


class ProprietaireViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    queryset = Proprietaire.objects.all()
    serializer_class = ProprietaireSerializers

