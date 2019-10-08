"""Customuser models."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager class."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create User with the given email."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create user."""
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create superuser."""
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Abtract user Model."""

    username = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        """User representation."""
        return '{}'.format(self.email)


class UserProfile(models.Model):
    """User Profile."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)

    def create_user_profile(sender, instance, created, **kwargs):
        """Save create user profile."""
        if created:
            UserProfile.objects.create(user=instance)

    def save_user_profile(sender, instance, **kwargs):
        """Save user profile."""
        instance.userProfile.save()
