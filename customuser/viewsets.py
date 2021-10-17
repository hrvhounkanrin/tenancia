"""Customuser app viewsets."""
import json
import logging
import os

import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from django.shortcuts import redirect, get_object_or_404
from requests.exceptions import HTTPError
from rest_framework import permissions, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from social_django.utils import psa

from client.models import Client
from client.serializers import ClientSerializer
from customuser.models import User
from customuser.serializers import SocialSerializer, UserSerializer
from proprietaire.models import Proprietaire
from proprietaire.serializers import ProprietaireSerializers
from societe.models import RealEstate
from societe.serializers import SocieteSerializer
from tools.viewsets import ActionAPIView
from proprietaire.viewsets import ProprietairAction
from .token_generator import TokenGenerator

logger = logging.getLogger(__name__)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


class CustomUserAction(ActionAPIView):
    def __init__(self):
        self.permission_classes = [permissions.AllowAny]

    @psa()
    def exchange_token(self, request, params={}, *args, **kwargs):

        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                nfe = settings.NON_FIELD_ERRORS_KEY
            except AttributeError:
                nfe = "non_field_errors"

            try:
                user = request.backend.do_auth(
                    serializer.validated_data["access_token"]
                )
            except HTTPError as e:
                payload = {"errors": {"token": "Invalid token", "detail": str(e)}}
                return {"success": False, "payload": payload}

            if user:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    payload = {"token": token.key}
                    return {"success": True, "payload": payload}
                else:
                    payload = {"errors": {nfe: "This user account is inactive"}}
                    return {"success": False, "payload": payload}

            else:
                payload = {"errors": {nfe: "Authentication Failed"}}
                return {"success": False, "payload": payload}

    def googleauth(self, request, params={}, *args, **kwargs):
        """Rigth func for google auth"""
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        """
        data = dict(client_id=request.data['clientId'],
                    redirect_uri=request.data['redirectUri'],
                    client_secret=settings.GOOGLE_SECRET,
                    code=request.data['code'],
                    grant_type='authorization_code')
        """
        data = dict(
            client_id=os.environ.get("CLIENT_ID"),
            redirect_uri=request.data["redirectUri"],
            client_secret=os.environ.get("GOOGLE_SECRET"),
            refresh_token=request.data["access_token"],
            grant_type="refresh_token",
        )
        r = requests.post(os.environ.get("ACCESS_TOKEN_URL"), data=data)
        token = json.loads(r.text)
        headers = {
            "Authorization": "Bearer {}".format(token["access_token"]),
            "Content-Type": "application/json; UTF-8",
        }
        # return Response({'token': token}, status.HTTP_201_CREATED)
        settings.PEOPLE_API_URL = "https://www.googleapis.com/oauth2/v3/userinfo?access_token={}".format(
            token["access_token"]
        )
        r = requests.get(settings.PEOPLE_API_URL, headers=headers)
        profile = json.loads(r.text)
        try:
            user = User.objects.get(email=profile["email"])
        except User.DoesNotExist:
            user = None

        if user is None:
            user = User.objects.create_user(
                username=profile["email"],
                first_name=profile["given_name"],
                last_name=profile["family_name"],
                email=profile["email"],
                password="teancia@2020",
            )

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        serializer = UserSerializer(user)
        print(f"payload: {payload}")
        print(f"token: {token}")
        # serializer.send_activation_mail(user)
        return Response({"token": token, "user": serializer.data}, status.HTTP_200_OK)

    def activate_account(self, request, params={}, *args, **kwargs):
        uidb64 = request.data["uidb64"]
        token = request.data["token"]
        uid = urlsafe_base64_decode(uidb64.strip()).decode()
        user = User.objects.get(pk=uid)

        account_activation_token = TokenGenerator()
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            logger.info(f"User account activation successfuly: {user.email}")
            payload = jwt_payload_handler(user)
            """
                return Response({
                    'token': jwt_encode_handler(payload),
                    'user': user
                })
            """
            # Should be redirected to the frontend login page instead.
            return {
                "success": True,
                "token": jwt_encode_handler(payload),
                "user": UserSerializer(user, context={"request": request}).data,
            }

        else:
            return {
                "success": False,
                "payload": "Une erreur est survenue. Merci de reessayer.",
            }


"""Get connected user profiles"""


class ProfileAction(ActionAPIView):
    def __get_profile(self, user_id):
        User = get_user_model()
        try:
            user = User.objects.get(pk=user_id)
            user_serializer = UserSerializer(user)
            proprietaire = Proprietaire.objects.filter(user__id=user_id).first()
            lessor_serializer = ProprietaireSerializers(proprietaire)
            client = Client.objects.filter(user__id=user_id).first()
            real_estate = RealEstate.objects.filter(created_by=user_id).first()
            client_serializer = ClientSerializer(client)
            profiles = {**user_serializer.data}
            if proprietaire is not None:
                lessor_data = lessor_serializer.data
                lessor_data.pop('user', None)
                profiles.update({"lessor": lessor_data})
            if client is not None:
                tenant_data = client_serializer.data
                tenant_data.pop('user', None)
                profiles.update({"tenant": tenant_data})
            if real_estate is not None:
                real_estate_serialiser = SocieteSerializer(real_estate)
                real_estate_data = real_estate_serialiser.data
                real_estate_data.pop('user', None)
                profiles.update({"real_estate": real_estate_data})
            return {"success": True, "payload": profiles}
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            serializer = UserSerializer(user)
            return {"success": True, "payload": serializer.data}
        else:
            return {"success": False, "msg": "An error occured."}

    def get_profile(self, request, params={}, *args, **kwargs):
        """Get all user profile."""
        return self.__get_profile(request.user.id)

    def create_profile(self, request, params={}, *args, **kwargs):
        data = request.data
        profile_type = data.pop('profile_type', None)
        if profile_type is None or profile_type not in ['lessor', 'tenant', 'real_estate']:
            return {"success": False, "payload": {"message": "Il manque le type de profil"}}

        serializer_context = {
            "request": request,
        }
        data["user_id"] = request.user.id
        if profile_type == 'lessor':
            serializer = ProprietaireSerializers(data=data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            serializer.save(created_by=request.user)

        if profile_type == 'tenant':
            serializer = ClientSerializer(data=data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if profile_type == 'real_estate':
            serializer = SocieteSerializer(data=data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return self.__get_profile(data["user_id"])

    def update_profile(self, request, params={}, *args, **kwargs):
        data = request.data
        profile_type = data.pop('profile_type', None)
        if profile_type is None or profile_type not in ['lessor', 'tenant', 'real_estate']:
            return {"success": False, "payload": {"message": "Il manque le type de profil"}}

        serializer_context = {
            "request": request,
        }
        data["user_id"] = request.user.id
        if profile_type == 'lessor':
            instance = get_object_or_404(Proprietaire, pk=params.get("id", None))
            data = request.data
            data["user_id"] = request.user.id
            serializer = ProprietaireSerializers(
                instance, data=request.data, context=serializer_context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(modified_by=request.user)

        if profile_type == 'tenant':
            serializer = ClientSerializer(data=data, context=serializer_context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        if profile_type == 'real_estate':
            instance = get_object_or_404(RealEstate, pk=params.get("id", None))
            serializer = SocieteSerializer(
                instance, data=request.data, context=serializer_context
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return self.__get_profile(data["user_id"])





