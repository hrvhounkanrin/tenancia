
import os
import requests
import json
from django.conf import settings
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.generics import CreateAPIView
from requests.exceptions import HTTPError
from social_django.utils import psa
from customuser.serializers import UserSerializer, PasswordResetSerializer
from django.utils.translation import gettext as _

from customuser.models import User


from .serializers import SocialSerializer

class CreateUSerApiView(APIView):
    """Customuser apiview."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Create user."""
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer_context = {"request": request}
        serializer.save()
        return Response(
            serializer.data,
            context=serializer_context,
            status=status.HTTP_201_CREATED,
        )


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
            status=status.HTTP_200_OK,
        )


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
        # Obteniendo datos de perfil
        """
        r = requests.get(settings.PEOPLE_API_URL, headers=headers)
        profile = json.loads(r.text)
        print(profile['email'])
        try:
            user = User.objects.get(email=profile['email'])
        except User.DoesNotExist:
            user = None

        if user:
            payload = TokenObtainPairSerializer(user)
            token = TokenObtainPairSerializer(payload)
            return Response({'token': token}, status.HTTP_200_OK)

        else:
            user = User.objects.create_user(username=profile['given_name'], email=profile["email"], password="nexo2016")
            # paciente = Paciente(user=user, pic_profile=profile['picture'], google_sub=profile['sub'])
            # paciente.save()
            # send_email_welcome(user)
            payload = TokenObtainPairSerializer(user)
            # token = JWT_ENCODE(payload)
            return Response({'token': token}, status.HTTP_201_CREATED)
        """


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
