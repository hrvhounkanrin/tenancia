"""Customuser views."""
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from customuser.serializers import (UserSerializer,
                                    PasswordResetSerializer)
from django.utils.translation import gettext as _


class CreateUSerApiView(APIView):
    """Customuser apiview."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Create user."""
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer_context = {
            'request': request,
        }
        serializer.save()
        return Response(serializer.data,
                        context=serializer_context,
                        status=status.HTTP_201_CREATED)


class PasswordResetView(GenericAPIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        """Send reinitialisation mail."""
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK
        )
