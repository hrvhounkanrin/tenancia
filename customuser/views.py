import os
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext as _
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

# Create your views here.
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView, status
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken, jwt_response_payload_handler

from customuser.decorators import method_decorator
from customuser.models import User

from .permissions import IsAdminUser, IsLoggedInUserOrAdmin
from .serializers import (
    PasswordChangeSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetSerializer,
    UserSerializer,
)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
# Create your views here.

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        "password", "old_password", "new_password1", "new_password2"
    )
)


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        "token": token,
        "user": UserSerializer(user, context={"request": request}).data
        # 'token_validty':timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
    }


from .token_generator import TokenGenerator


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == "create":
            permission_classes = [AllowAny]
        elif (
            self.action == "retrieve"
            or self.action == "update"
            or self.action == "partial_update"
        ):
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == "list" or self.action == "destroy":
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


# Create your views here.


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    def post(self, request):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # pass the 'raise_exception' flag
        user = serializer.object.get("user") or request.user
        print("CustomObtainJSONWebToken Ok")

        """
        serializer.is_valid(raise_exception=True) # pass the 'raise_exception' flag
        user = serializer.object.get('user') or request.user
        token = serializer.object.get('token')
        response_data = jwt_response_payload_handler(token, user, request)
        """
        # Should be redirected to the frontend login page instead.
        payload = jwt_payload_handler(user)
        ini_time_for_now = datetime.now()
        now = datetime.now()

        timestamp = datetime.timestamp(now)
        return Response(
            {
                "expire_in": 20,
                "token": jwt_encode_handler(payload),
                "user": UserSerializer(user, context={"request": request}).data,
            }
        )
        return Response(response_data)


class PasswordResetView(GenericAPIView):
    """
    Accepts the following POST parameters: email
    Returns the success/fail message.
    """

    serializer_class = PasswordResetSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        """
        Validate the request and send Password reset e-mail
        :param request:
        :return: Password reset e-mail  or error message
        """
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        # Return the success message with OK HTTP status
        return Response(
            {"detail": _("Password reset e-mail has been sent.")},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (permissions.AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """
        Confirm the password reset
        :param request:
        :return: Password reset confirm or error message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("Password has been reset with the new password.")})


class PasswordChangeView(GenericAPIView):
    """
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """

    serializer_class = PasswordChangeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request):
        """
        Save new password and send password change e-mail
        :param request:
        :return: New password has been saved and e-mail or error message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": _(
                    "New password " "has been saved and e-mail " "has been sent.."
                )
            }
        )


class LogoutView(APIView):
    """
    Calls Django logout method and delete the Token object
    assigned to the current User object.

    Accepts/Returns nothing.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [JSONWebTokenAuthentication]

    def post(self, request):
        """
        post method to logout
        :param request:
        :return:
        """
        return self.logout(request)

    def logout(self, request):
        """
        logout the user
        :param request:
        :return:
        """
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        django_logout(request)

        return Response(
            {"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK
        )


class ActivateAccount(GenericViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["post"], detail=False, permission_classes=(AllowAny,))
    def activate_account(self, request, *args, **kwargs):
        uidb64 = request.query_params.get("uidb64", None)
        token = request.query_params.get("token", None)
        if uidb64 is None or token is None:
            return Response(
                {"success": False, "payload": "Un ou plusieurs paramètres manquent."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            uid = urlsafe_base64_decode(uidb64.strip()).decode()
        except:
            return Response(
                {
                    "success": False,
                    "payload": "Un ou plusieurs paramètres sont incorrects.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.get(pk=uid)

        account_activation_token = TokenGenerator()
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            payload = jwt_payload_handler(user)
            """
                return Response({
                    'token': jwt_encode_handler(payload),
                    'user': user
                })
            """
            # Should be redirected to the frontend login page instead.
            return Response(
                {
                    "success": True,
                    "expire_in": settings.JWT_AUTH["JWT_EXPIRATION_DELTA"],
                    "token": jwt_encode_handler(payload),
                    "user": UserSerializer(user, context={"request": request}).data,
                }
            )

        else:
            return Response(
                {
                    "success": False,
                    "payload": "Une erreur est survenue. Merci de reessayer.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
