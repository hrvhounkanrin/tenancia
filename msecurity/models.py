import jwt
from django.db import models
from model_utils import Choices
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework_jwt.utils import jwt_payload_handler

class UserManager(BaseUserManager):
  
    def create_user(self,**validated_data ):
        username=validated_data.get('username', None)
        password=validated_data.get('password', None)
        email=validated_data.get('email', None)
        first_name=validated_data.get('first_name', None)
        last_name=validated_data.get('last_name', None)
        num_telephone=validated_data.get('num_telephone', None)
        sexe=validated_data.get('sexe', None)
        type_personne=validated_data.get('type_personne', None)
        adresse_residence=validated_data.get('adresse_residence', None)
        ville=validated_data.get('ville', None)
        pays=validated_data.get('pays', None)
        code_postal=validated_data.get('code_postal', None)
        date_naissance=validated_data.get('date_naissance', None)
        
        
        if email is None:
            raise TypeError('Users must have an email address.')
        
        if num_telephone is None:
            raise TypeError('Users must have a phone number.')

        user = self.model(username=username, 
                          email=self.normalize_email(email),
                          first_name=first_name,
                          last_name=last_name,
                          num_telephone=num_telephone,
                          sexe=sexe,
                          type_personne=type_personne,
                          ville=ville,
                          code_postal=code_postal,
                          pays=pays,
                          adresse_residence=adresse_residence,
                          date_naissance=date_naissance)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, **validated_data):
        """
        Create and return a 'User' with superuser (admin) permissions.
        """
        password=validated_data.get('password', None)
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(**validated_data)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

class User(AbstractBaseUser, PermissionsMixin):
   
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    sexe = models.CharField(max_length=50, null=True)
    num_telephone=models.CharField(max_length=20, null=False, unique=True)
    first_name=models.CharField(max_length=150, null=True)
    last_name=models.CharField(max_length=150, null=True)
    type_personne=models.CharField(max_length=20, null=True)
    date_naissance=models.DateField(null=True)
    adresse_residence=models.CharField(max_length=100, null=True)
    code_postal=models.CharField(max_length=50, null=True)
    ville=models.CharField(max_length=100, null=True)
    pays=models.CharField(max_length=50, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'num_telephone' ]

    def __str__(self):
       
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling 'user.token' instead of
        'user.generate_jwt_token().
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return self.username

    def get_short_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first name.
        """
        return self.first_name

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
       """
        payload = jwt_payload_handler(self)
        token = jwt.encode(payload, settings.SECRET_KEY)
        return token.decode('unicode_escape')


class UserLoginActivity(models.Model):
    # Login Status
    SUCCESS = 'S'
    FAILED = 'F'

    LOGIN_STATUS = ((SUCCESS, 'Success'),
                           (FAILED, 'Failed'))

    login_IP = models.GenericIPAddressField(null=True, blank=True)
    login_datetime = models.DateTimeField(auto_now=True)
    login_username = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=1, default=SUCCESS, choices=LOGIN_STATUS, null=True, blank=True)
    user_agent_info = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'user_login_activity'
        verbose_name_plural = 'user_login_activities'