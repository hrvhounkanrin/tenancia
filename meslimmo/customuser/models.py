from django.db import models
from __future __ import unicode_literals
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUSer, PermissionMixin
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.utils.http import urlquote



# Create your models here.

class AccountManager(BaseUserManager):

	def create_user(self, email, password, is_staff, **extra_fields):
		"""
		Creates and saves a User with the given email and password.
		"""
		now = timezone.now()
		if not email:
			raise ValueError('The given email must be set')
		email = self.normalize_email(email)
		user = self.model(email=email,
			is_staff=is_staff, is_active=True,
			is_superuser=is_superuser, last_login=now,
			date_joined=now, **extra_fields)
		user.set_password(password)
		user.user_type =1
		user.save(using=self._db)
		return user


    def create_user(self, email, password=None, **extra_fields):
    return self._create_user(email, password, False, False,
                             **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class UserType(models.Model):

    name = models.CharField(max_length=32)

    class Meta:
        verbose_name = "User Type"
        verbose_name_plural = "User Types"

    def __str__(self):
        return self.name
