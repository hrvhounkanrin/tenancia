"""Immeuble app models."""
from random import randint

from countries_plus.models import Country
from django.conf import settings
from django.db import models
from django.db.models import Count


class Immeuble(models.Model):
    """Immeuble model."""

    intitule = models.CharField(max_length=50)
    description = models.CharField(
        max_length=512,
        null=True,
    )
    adresse = models.CharField(
        max_length=512,
        null=True,
    )
    proprietaire = models.ForeignKey(
        "proprietaire.Proprietaire", on_delete=models.CASCADE, null=True
    )

    jour_emission_facture = models.IntegerField(default=5)
    jour_valeur_facture = models.IntegerField(default=5)
    ville = models.CharField(max_length=128, null=True)
    quartier = models.CharField(max_length=128, null=True)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    longitude = models.DecimalField(max_digits=20, decimal_places=12)
    latitude = models.DecimalField(max_digits=20, decimal_places=12)
    ref_immeuble = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    nb_etage = models.IntegerField(default=0)
    realestate = models.ForeignKey(
        'societe.RealEstate',
        null=True,
        on_delete=models.SET_NULL,
        editable=True,
        related_name="realestate_managed",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="immeuble_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="immeuble_updated_user",
    )

    def __str__(self):
        """Immeuble reprensentation."""
        return f"{self.intitule} {self.proprietaire.user.last_name}"

    class Meta:
        """Immeuble model meta."""
        ordering = ['-id']
        verbose_name = "Immeuble"
        verbose_name_plural = "Immeubles"


class AutoNameManager(models.Manager):
    def random(self):
        count = self.aggregate(ids=Count("id"))["ids"]
        random_index = randint(0, count - 1)
        return self.all()[random_index]

    def random_naive(self):
        return self.all().order_by("?")[0]


class AutoName(models.Model):
    libelle = models.CharField(max_length=50, null=False)
    observation = models.CharField(max_length=50, default="city")

    objects = AutoNameManager()

    def __str__(self):
        """Random autoname."""
        return "%s" % (self.libelle)
