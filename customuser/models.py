from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager

class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name','num_telephone','username' ]


    email = models.EmailField(max_length=255, unique=True)
    num_telephone=models.CharField(max_length=20, null=True)
    username=models.CharField(max_length=50, null=True)
    date_naissance=models.DateField(null=True)
    adresse_residence=models.CharField(max_length=100, null=True)
    code_postal=models.CharField(max_length=50, null=True)
    ville=models.CharField(max_length=100, null=True)
    pays=models.CharField(max_length=50, null=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def get_short_name(self):
        return self.username

    def __str___(self):
        return self.email


