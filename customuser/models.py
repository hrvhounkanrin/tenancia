from __future__ import unicode_literals
from django.db import models, transaction
# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin, BaseUserManager)



class UserManager(BaseUserManager):
    def __create_user(self, email, password, **extra_fields):
        """
         This  function creates and saves the USer with the given
         Email and password
         Cette function reecrite sauvergarde tout simplement le ni
         d'utilisteur et  son email

        :param email:
        :param password:
        :return:
        """
        if not email:
            # si pas d'eamil  l'erreur doit etre lancee pour
            # afficher qu'il n'y a pas d'email
            raise ValueError('The email given must be set ')
        try:
            with transaction.atomic():
                user=self.model(email=email, **extra_fields)
                user.set_password(password)
                user.save(using=self._db)
                return user
        except:
            raise


    def create_user(self, email, password=None, **extra_fields):
        """
         Cree l'utilisateur
         #verifie si l'utilsateur est un staff
         #verifie si tuilisateur est un super_user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self.__create_user(email, password, **extra_fields)


    def create_superuser(self, email, password, **extra_fields):
        """
         Create super user
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.__create_user(email, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
     This  Abstract Class will implement a fully featureed
     Admin -compliant permissions
    """
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []