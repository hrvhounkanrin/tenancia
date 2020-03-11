"""Customuser viewset."""
import logging

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from customuser.models import User
from customuser.permissions import IsAdminUser
from customuser.permissions import IsLoggedInUserOrAdmin
from customuser.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """User Serializer Class ViewSet."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    logging.debug(f'user serializer class, {serializer_class}')

    def get_permissions(self):
        """
        Set up class permission.

        :return:
        """
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or\
                self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
