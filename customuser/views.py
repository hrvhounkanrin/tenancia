
import os
import requests
import json
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView
from requests.exceptions import HTTPError
from social_django.utils import psa
from django.utils.translation import gettext as _
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import (
    logout as django_logout
)
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.
from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import status, APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework.decorators import action
from customuser.decorators import method_decorator
from customuser.models import User
from .permissions import (
    IsLoggedInUserOrAdmin,
    IsAdminUser
)
from .serializers import (
    UserSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer
)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
jwt_get_username_from_payload = api_settings.JWT_PAYLOAD_GET_USERNAME_HANDLER
# Create your views here.

sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2'
    )
)

from .serializers import SocialSerializer
from .token_generator import TokenGenerator

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve' or \
                self.action == 'update' or \
                self.action == 'partial_update':
            permission_classes = [IsLoggedInUserOrAdmin]
        elif self.action == 'list' or self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

# Create your views here.
def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }


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
            status=status.HTTP_200_OK
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
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request):
        """
        Confirm the password reset
        :param request:
        :return: Password reset confirm or error message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": _("Password has been reset with the new password.")}
        )

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
        return super(PasswordChangeView, self).dispatch(*args, **kwargs)

    def post(self, request):
        """
        Save new password and send password change e-mail
        :param request:
        :return: New password has been saved and e-mail or error message
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": _("New password "
                                     "has been saved and e-mail "
                                     "has been sent.."
                                     )})

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

        return Response({"detail": _("Successfully logged out.")},
                        status=status.HTTP_200_OK)

class ActivateAccount(GenericViewSet):
    permission_classes = (AllowAny,)

    @action(methods=["post"], detail=False, permission_classes=(AllowAny,))
    def activate_account(self, request, *args, **kwargs):
        uidb64 = request.query_params['uidb64']
        token = request.query_params['token']
        uid = urlsafe_base64_decode(uidb64.strip()).decode()
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
            return Response({
                'success': True,
                'token': jwt_encode_handler(payload),
                'user': UserSerializer(user, context={'request': request}).data
            })

        else:
            return Response({'success': False, 'payload': 'Une erreur est survenue. Merci de reessayer.'}, status=status.HTTP_400_BAD_REQUEST)

# https://stackoverflow.com/questions/48460331/how-to-make-social-login-with-drf-as-backend-and-angularjs-as-frontend-and-drf-r
class AuthGoogleView(CreateAPIView):

    def post(self, request):
        """
        data = dict(client_id=request.data['clientId'],
                    redirect_uri=request.data['redirectUri'],
                    client_secret=settings.GOOGLE_SECRET,
                    code=request.data['code'],
                    grant_type='authorization_code')
        """
        data = dict(client_id=os.environ.get("CLIENT_ID"),
                    redirect_uri=request.data['redirectUri'],
                    client_secret=os.environ.get("GOOGLE_SECRET"),
                    code=request.data['code'],
                    grant_type='authorization_code')
        print(data)
        print(settings.ACCESS_TOKEN_URL)
        # Obteniendo Access Token
        r = requests.post(os.environ.get("ACCESS_TOKEN_URL"), data=data)
        token = json.loads(r.text)
        print(token)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token'])}
        return Response({'token': token}, status.HTTP_201_CREATED)


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
@psa()
def exchange_token(request, backend):
    """
    Exchange an OAuth2 access token for one for this site.

    This simply defers the entire OAuth2 process to the front end.
    The front end becomes responsible for handling the entirety of the
    OAuth2 process; we just step in at the end and use the access token
    to populate some user identity.

    The URL at which this view lives must include a backend field, like:
        url(API_ROOT + r'social/(?P<backend>[^/]+)/$', exchange_token),

    Using that example, you could call this endpoint using i.e.
        POST API_ROOT + 'social/facebook/'
        POST API_ROOT + 'social/google-oauth2/'

    Note that those endpoint examples are verbatim according to the
    PSA backends which we configured in settings.py. If you wish to enable
    other social authentication backends, they'll get their own endpoints
    automatically according to PSA.

    ## Request format

    Requests must include the following field
    - `access_token`: The OAuth2 access token provided by the provider
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = 'non_field_errors'

        try:
            # this line, plus the psa decorator above, are all that's necessary to
            # get and populate a user object for any properly enabled/configured backend
            # which python-social-auth can handle.
            print('Try serializer')
            user = request.backend.do_auth(serializer.validated_data['access_token'])
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {'errors': {
                    'token': 'Invalid token',
                    'detail': str(e),
                }},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            if user.is_active:
                token, _ = Token.objects.get_or_create(user=user)
                return Response({'token': token.key})
            else:
                # user is not active; at some point they deleted their account,
                # or were banned by a superuser. They can't just log in with their
                # normal credentials anymore, so they can't log in with social
                # credentials either.
                return Response(
                    {'errors': {nfe: 'This user account is inactive'}},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.
            return Response(
                {'errors': {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
