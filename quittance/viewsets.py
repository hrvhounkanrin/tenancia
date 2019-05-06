from tools.viewsets import  ActionAPIView
from  quittance.models import  *
from quittance.serializers import  *
from rest_framework.viewsets import  ModelViewSet


class QuittanceActionViewSet(ActionAPIView):

    def get_quittances(self, request, params ={} , *args, **kwargs):
        """  The simplest way to  get the list of all the quittances"""
        get_all_quittances_ = Quittance.objects.all()
        ser_quittance = QuittanceSerializers(get_all_quittances_, many=True).data
        return {"success":True, "quittances":ser_quittance }
    get_quittances.__doc__ =  "The simple way to get the list of all the quittanceb using the APIActionViewSet"



    def get_client_per_invoice(self,request,  params={} , *args, **kwargs):

        """
         test
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        get_all_quittances_ = Quittance.objects.all()
        ser_quittance = QuittanceSerializers(get_all_quittances_, many=True).data
        return {"success":True, "quittances":ser_quittance }
