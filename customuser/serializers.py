"""Customuser serializer."""
import logging
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import IntegrityError, transaction
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework import serializers
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from customuser.models import User
from customuser.models import UserProfile
from .token_generator import account_activation_token

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class UserProfileSerializer(serializers.ModelSerializer):
    """Userprofil serializer."""

    class Meta:
        """Userprofil serializer meta."""

        model = UserProfile
        fields = ('dob', 'title', 'address', 'country', 'photo')


class UserSerializer(serializers.ModelSerializer):
    """Userserializer class."""

    profile = UserProfileSerializer(required=False)

    class Meta:
        """Userserializer meta."""

        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """User serializer create."""
        profile_data = validated_data.pop('profile')
        logging.debug(f'**Profile  data information', f'{profile_data}')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        self.send_activation_mail(user)
        return user

    def send_activation_mail(self, user):
        """Send activation mail to user."""
        token = account_activation_token.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        msg_content = render_to_string('activate_account.html', {
            'user': user,
            'domain': 'https://tenancia.com',
            'uid': uid,
            'token': token,
        })
        to_email = user.email
        message = Mail(
            from_email='noreply@tenancia.com',
            to_emails=to_email,
            subject='Activation de votre compte',
            html_content=msg_content)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            sg.send(message)
            return True
        except Exception as e:
            logging.debug(f'**Profile  data information', f'{e}')
            return False

    def update(self, instance, validated_data):
        """Customuser update."""
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        profile.title = profile_data.get('title', profile.title)
        profile.dob = profile_data.get('dob', profile.dob)
        profile.address = profile_data.get('address', profile.address)
        profile.country = profile_data.get('country', profile.country)
        profile.city = profile_data.get('city', profile.city)
        profile.zip = profile_data.get('zip', profile.zip)
        profile.photo = profile_data.get('photo', profile.photo)
        profile.save()
        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    """Override djoser create user serializer."""

    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)
    profile = UserProfileSerializer(required=False)
    default_error_messages = {
        "cannot_create_user": _("Unable to create account.")
    }

    class Meta:
        """User create serializer meta."""

        model = User
        fields = ('id', 'email', 'first_name',
                  'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        """Validate."""
        attrs.pop('profile', None)
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error["non_field_errors"]}
            )

        return attrs

    def create(self, validated_data):
        """Perform create."""
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        return user

    def perform_create(self, validated_data):
        """Perform create."""
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            profile_data = self.initial_data.get('profile', None)
            if profile_data:
                UserProfile.objects.create(user=user, **profile_data)
        return user
