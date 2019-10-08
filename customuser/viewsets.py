"""Customuser viewset."""
import logging
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from customuser.models import User
from customuser.permissions import IsAdminUser
from customuser.permissions import IsLoggedInUserOrAdmin
from customuser.serializers import UserSerializer
from django.contrib.auth import get_user_model
from .token_generator import account_activation_token


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


class AccountViewset(GenericViewSet):
    """Account activation viewset."""

    permission_classes = (AllowAny,)
    @action(methods=["get"], detail=False, permission_classes=(AllowAny,))
    def activate_account(self, request, uidb64, token):
        """Account activation."""
        User = get_user_model()
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and \
                account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            serializer = UserSerializer(user)
            return {'success': True, 'user': serializer}
        else:
            return {'success': False, 'msg': 'An error occured.'}
