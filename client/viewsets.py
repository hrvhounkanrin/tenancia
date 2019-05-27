from rest_framework import permissions
from tools.viewsets import GenericModelSerializer

import json
from  tools.viewsets import ActionAPIView
from appartement.models import Appartement
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response

from .models import Client

from rest_framework import views, viewsets, authentication, permissions, mixins, pagination
from  client.serializers import ClientSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets

class ClientViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

"""
class ClientViewSet(viewsets.ViewSet):
    # @permission_classes((permissions.AllowAny,))
    def list(self, request, *args, **kwargs):
        #v1 works with this end/point
        queryset = Client.objects.all()
        print (queryset)
        return Response(ClientSerializer(queryset, many=True).data)
    # @determine_staff
    def list_all_client(self, request, *args, **kwargs):
        #v1 works with this end/point
        queryset = Client.objects.all()
        print (queryset)
        return Response({'success':True},ClientSerializer(queryset, many=True).data)
"""
    # @classmethod
    # def get_extra_actions(cls):
    #     return []