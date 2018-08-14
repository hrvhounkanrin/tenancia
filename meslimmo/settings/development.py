import datetime
from meslimmo.settings.commons import *
import os

DATABASES = {
    'default': {
        'ENGINE': os.environ['DATABASE_ENGINE'],
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USER'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],   # Or an IP Address that your DB is hosted on
        'PORT': os.environ['DATABASE_PORT'],
    }
}

DEBUG = True

REST_REGISTRATION = {
    'USER_LOGIN_FIELDS': 'email',
    'USER_HIDDEN_FIELDS': (
        'is_active',
        'is_staff',
        'is_superuser',
        'user_permissions',
        'groups',
        'date_joined',
    ),
    'USER_PUBLIC_FIELDS': 'first_name',
    'USER_EMAIL_FIELD': 'email',

    'USER_VERIFICATION_FLAG_FIELD': 'is_active',

    'REGISTER_SERIALIZER_CLASS': 'rest_registration.api.serializers.DefaultRegisterUserSerializer',
    'REGISTER_SERIALIZER_PASSWORD_CONFIRM': True,

    'REGISTER_VERIFICATION_ENABLED': True,
    'REGISTER_VERIFICATION_PERIOD': datetime.timedelta(days=7),
    'REGISTER_VERIFICATION_URL': 'https://africa-rentings/verify-user/',
    'REGISTER_VERIFICATION_EMAIL_TEMPLATES': {
        'subject':  'rest_registration/register/subject.txt',
        'body':  'rest_registration/register/body.txt',
    },

    'LOGIN_SERIALIZER_CLASS': 'rest_registration.api.serializers.DefaultLoginSerializer',
    'LOGIN_AUTHENTICATE_SESSION': None,
    'LOGIN_RETRIEVE_TOKEN': None,

    'RESET_PASSWORD_VERIFICATION_PERIOD': datetime.timedelta(days=1),
    'RESET_PASSWORD_VERIFICATION_URL': 'https://africa-rentings/reset-password/',
    'RESET_PASSWORD_VERIFICATION_EMAIL_TEMPLATES': {
        'subject': 'rest_registration/reset_password/subject.txt',
        'body': 'rest_registration/reset_password/body.txt',
    },

    'REGISTER_EMAIL_VERIFICATION_ENABLED': True,
    'REGISTER_EMAIL_VERIFICATION_PERIOD': datetime.timedelta(days=7),
    'REGISTER_EMAIL_VERIFICATION_URL': 'https://africa-rentings/verify-user/',
    'REGISTER_EMAIL_VERIFICATION_EMAIL_TEMPLATES': {
        'subject':  'rest_registration/register_email/subject.txt',
        'body':  'rest_registration/register_email/body.txt',
    },

    'CHANGE_PASSWORD_SERIALIZER_PASSWORD_CONFIRM': True,

    'PROFILE_SERIALIZER_CLASS': 'msecurity.serializers.UserSerializer',

    'VERIFICATION_FROM_EMAIL': 'noreply@sahges.com',
    'VERIFICATION_REPLY_TO_EMAIL': 'noreply@sahges.com',
    'VERIFICATION_EMAIL_HTML_TO_TEXT_CONVERTER': 'rest_registration.utils.convert_html_to_text_preserving_urls',

    'SUCCESS_RESPONSE_BUILDER': 'rest_registration.utils.build_default_success_response',
}