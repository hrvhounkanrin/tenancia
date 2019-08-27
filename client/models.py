from django.conf import settings
from django.db import models


class Client(models.Model):
    nom = models.CharField(max_length=132, null=True, blank=True)
    prenom = models.CharField(max_length=132, null=True, blank=True)
    mode_paiement = models.CharField(max_length=64, null=True, blank=True)
    profession = models.CharField(max_length=128, null=True, blank=True)
    ice_contact = models.CharField(max_length=128, null=True, blank=False)
    ice_number = models.CharField(max_length=28, null=True, blank=False)
    ice_relation = models.CharField(max_length=64, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, )
    banque = models.ForeignKey('banque.Banque', on_delete=models.SET_NULL, null=True, )

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
