# -*- coding: UTF-8 -*-
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from .serializers import BanqueSerializers
from .models import Banque



class BanqueViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = Banque.objects.all()
    serializer_class = BanqueSerializers

