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
        serialized_obj = ProprietaireSerializers(proprio_all, many=True).data
        return {"success": True, "payload": serialized_obj}

    def create_proprio(self, request, param={}, *args, **kwargs):
        """
         Create proprio based on existing user
        :param request:
        :param params:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(request.data.get('proprietaire', None), list):
            print("Liste de proprietaire")
            proprietaires = request.data.pop('proprietaire')
            proprietaire_objects = []
            for proprio in proprietaires:
                serializer = ProprietaireSerializers(data=proprio)
                serializer.is_valid(raise_exception=True)
                proprietaire_objects.append(serializer)
            saved_proprio = [model.save() for model in proprietaire_objects]
            serialized_proprio = ProprietaireSerializers(saved_proprio, many=True)
            return {"success": True, "proprietaire": serialized_proprio.data}

        #print(request.data.pop('user'))
        serializer = ProprietaireSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return {"success": True, "proprietaire": serializer.data}
