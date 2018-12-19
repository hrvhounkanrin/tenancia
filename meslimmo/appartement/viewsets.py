import json
from  meslimmo.tools.viewsets import ActionAPIView
from meslimmo.appartement.models import Appartement
from django.http.response import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from meslimmo.appartement.serializers import AppartementSerializers
from rest_framework import views, viewsets, authentication, permissions, mixins, pagination
class GetAppartmentViewSet(ActionAPIView):
    # @determine_staff
    def list_all_appartment(self, request, *args, **kwargs):
        #v1 works with this end/point
        queryset = Appartement.objects.all()
        return Response(AppartementSerializers(queryset, many=True).data)