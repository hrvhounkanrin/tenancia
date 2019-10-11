"""Customuser serializer."""
import logging
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext as _
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


class PasswordResetSerializer(serializers.Serializer):
    """Custom password serializer."""

    email = serializers.EmailField()
    password_reset_form_class = PasswordResetForm

    def validate_email(self, value):
        """Validate user mail."""
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(_('Error'))

        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(_('Invalid e-mail address'))
        return value

    def save(self):
        """Save."""
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'subject_template_name':
                'registration/password_reset_subject.txt',
            'html_email_template_name':
                'registration/password_reset_email.html',
            'request': request,
        }
        self.reset_form.save(**opts)
