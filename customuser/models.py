from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


class User(AbstractUser):
    """ Abtract user Model."""

    username = models.CharField(max_length=128, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


class UserProfile(models.Model):
    """ User Profile."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    title = models.CharField(max_length=5)
    dob = models.DateField()
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5)
    photo = models.ImageField(upload_to='uploads', blank=True)






#
#
# class UserManager(BaseUserManager):
#     def __create_user(self, email, password, **extra_fields):
#         """
#          This  function creates and saves the USer with the given
#          Email and password
#          Cette function reecrite sauvergarde tout simplement le ni
#          d'utilisteur et  son email
#
#         :param email:
#         :param password:
#         :return:
#         """
#         if not email:
#             # si pas d'eamil  l'erreur doit etre lancee pour
#             # afficher qu'il n'y a pas d'email
#             raise ValueError('The email given must be set ')
#         try:
#             with transaction.atomic():
#                 user=self.model(email=email, **extra_fields)
#                 user.set_password(password)
#                 user.save(using=self._db)
#                 return user
#         except:
#             raise
#
#
#     def create_user(self, email, password=None, **extra_fields):
#         """
#          Cree l'utilisateur
#          #verifie si l'utilsateur est un staff
#          #verifie si tuilisateur est un super_user
#         :param email:
#         :param password:
#         :param extra_fields:
#         :return:
#         """
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self.__create_user(email, password, **extra_fields)
#
#
#     def create_superuser(self, email, password, **extra_fields):
#         """
#          Create super user
#         :param email:
#         :param password:
#         :param extra_fields:
#         :return:
#         """
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.__create_user(email, password=password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     """
#      This  Abstract Class will implement a fully featureed
#      Admin -compliant permissions
#     """
#     email = models.EmailField(max_length=40, unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(default=timezone.now)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
# from django.db import models
# from django.contrib.auth.models import AbstractUser, AbstractBaseUser, PermissionsMixin, UserManager
#
# """
# class User(AbstractUser):
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['last_name','num_telephone','username' ]
#
#
#     email = models.EmailField(max_length=255, unique=True)
#     num_telephone=models.CharField(max_length=20, null=True)
#     username=models.CharField(max_length=50, null=True)
#     date_naissance=models.DateField(null=True)
#     adresse_residence=models.CharField(max_length=100, null=True)
#     code_postal=models.CharField(max_length=50, null=True)
#     ville=models.CharField(max_length=100, null=True)
#     pays=models.CharField(max_length=50, null=False)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
#     time_created = models.DateTimeField(auto_now_add=True)
#     time_modified = models.DateTimeField(auto_now=True)
#
#     objects = UserManager()
#
#     def get_short_name(self):
#         return self.username
#
#     def __str___(self):
#         return self.email
#
# """
