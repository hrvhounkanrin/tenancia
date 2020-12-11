# -*- coding: UTF-8 -*-
"""Customuser app viewsets."""
import os
import logging
import requests
import json
from  django.conf import  settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from requests.exceptions import HTTPError
from social_django.utils import psa
from tools.viewsets import ActionAPIView
from proprietaire.models import Proprietaire
from client.models import Client
from customuser.models import User
from client.serializers import ClientSerializer
from proprietaire.serializers import ProprietaireSerializers
from customuser.serializers import SocialSerializer, UserSerializer
logger = logging.getLogger(__name__)


class CustomUserAction(ActionAPIView):

    """Customuser actionview."""
    def get_profile(self, request, params={}, *args, **kwargs):
        """Get all user profile."""
        User = get_user_model()
        try:
            user = User.objects.get(pk=request.user.id)
            print(user)
            serializer = UserSerializer(user)
            proprietaire = Proprietaire.objects.filter(
                user__id=request.user.id
            ).first()
            lessor_serializer = ProprietaireSerializers(proprietaire)
            client = Client.objects.filter(user__id=request.user.id).first()
            client_serializer = ClientSerializer(client)
            profiles = {"user": serializer.data}
            if proprietaire is not None:
                profiles.update({"bailleur": lessor_serializer.data})
            if client is not None:
                profiles.update({"locataire": client_serializer.data})
            return {"success": True, "profiles": profiles}
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
            serializer = UserSerializer(user)
            return {"success": True, "user": serializer.data}
        else:
            return {"success": False, "msg": "An error occured."}

    @psa()
    def exchange_token(self, request, params={}, *args, **kwargs):
        print('start exchange ok')
        serializer = SocialSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                nfe = settings.NON_FIELD_ERRORS_KEY
            except AttributeError:
                nfe = 'non_field_errors'

            try:
                user = request.backend.do_auth(serializer.validated_data['access_token'])
            except HTTPError as e:
                payload = {'errors': {
                        'token': 'Invalid token',
                        'detail': str(e),
                }}
                return {'success': False, 'payload': payload}

            if user:
                if user.is_active:
                    token, _ = Token.objects.get_or_create(user=user)
                    payload = {'token': token.key}
                    return {'success': True, 'payload': payload}
                else:
                    payload = {'errors': {nfe: 'This user account is inactive'}}
                    return {'success': False, 'payload': payload}

            else:
                payload = {'errors': {nfe: "Authentication Failed"}}
                return {'success': False, 'payload': payload}

    def googleauth(self, request, params={}, *args, **kwargs):
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
                    refresh_token=request.data['access_token'],
                    grant_type='refresh_token')
        # print(data)
        # print(os.environ.get("ACCESS_TOKEN_URL"))
        # Obteniendo Access Token
        r = requests.post(os.environ.get("ACCESS_TOKEN_URL"), data=data)
        token = json.loads(r.text)
        # print(token)
        headers = {'Authorization': 'Bearer {0}'.format(token['access_token']), 'Content-Type': 'application/json; UTF-8'}
        # return Response({'token': token}, status.HTTP_201_CREATED)
        # Obteniendo datos de perfil
        settings.PEOPLE_API_URL = 'https://www.googleapis.com/oauth2/v3/userinfo?access_token={}'.format(token['access_token'])
        r = requests.get(settings.PEOPLE_API_URL, headers=headers)
        profile = json.loads(r.text)
        # print(profile)
        try:
            user = User.objects.get(email=profile['email'])
        except User.DoesNotExist:
            user = None

        if user:
            token = Token.objects.get_or_create(user=user)
            print('Type de payload: {}-{}'.format(token[0], token[1]))
            print('Type de payload: {}-{}-{}'.format(token[0], type(token[0]), token[0].key))
            serializer = UserSerializer(user)
            # token = TokenObtainPairSerializer(payload.data)
            return Response({'token': token[0].key, 'user': serializer.data}, status.HTTP_200_OK)

        else:
            user = User.objects.create_user(username=profile['name'], first_name=profile['given_name'], last_name=profile['family_name'], email=profile["email"], password="teancia@2020")
            # paciente = Paciente(user=user, pic_profile=profile['picture'], google_sub=profile['sub'])
            # paciente.save()
            # send_email_welcome(user)
            token = Token.objects.get_or_create(user=user)
            serializer = UserSerializer(user)
            serializer.send_activation_mail(user)
            return Response({'token': token[0].key, 'user': serializer.data}, status.HTTP_201_CREATED)

