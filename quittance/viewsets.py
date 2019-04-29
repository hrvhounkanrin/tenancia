from tools.viewsets import  ActionAPIView
from  quittance.models import  *
from quittance.serializers import  *
from rest_framework.viewsets import  ModelViewSet


class QuittanceActionViewSet(ActionAPIView):

    def get_quittances(self, request, params ={} , *args, **kwargs):

        return {"success":False }