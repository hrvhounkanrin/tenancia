"""Proprietaire app models."""
from countries_plus.models import Country
from django.conf import settings
from django.db import models


class Proprietaire(models.Model):
    """Proprietaire model."""

    # utiliser un json field
    mode_paiement = models.CharField(max_length=50, null=False)
    numcompte = models.CharField(max_length=50, null=True)
    name_on_account = models.CharField(null=True, max_length=64)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
    )
    banque = models.ForeignKey(
        "banque.Banque",
        on_delete=models.SET_NULL,
        null=True,
    )
    numero_ifu = models.CharField(max_length=150, null=True)
    pays_residence = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="proprietaire_created_user",
    )
    phone_number = models.CharField(max_length=56, null=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="proprietaire_updated_user",
    )

    def _str__(self):
        """Proprietaire str representation."""
        return "{} {} ({})".format(self.user.first_name,self.user.last_name, self.phone_number )
