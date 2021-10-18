"""Mandataire app models."""
import os
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
def upload_to(instance, filename):
    # now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    #milliseconds = now.microsecond // 1000
    uid = str(uuid.uuid1())
    return f"realestate/{uid}{extension}"

class RealEstate(models.Model):
    """RealEstate model."""

    raison_social = models.CharField(max_length=150, null=False)
    num_telephone = models.CharField(max_length=50, null=False)
    adresse = models.CharField(max_length=150, null=True)
    logo = models.ImageField(upload_to=upload_to, null=True)
    num_carte_professionnel = models.CharField(max_length=150, null=True)
    numero_ifu = models.CharField(max_length=150, null=True)
    date_delivrance = models.DateField(null=True)
    carte_professionnel = models.FileField(upload_to="documents/", null=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="RealEstateUsers",
        related_name="users",
        blank=True,
    )
    mode_recouvrement = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name="societe_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        on_delete=models.CASCADE,
        related_name="societe_updated_user",
    )

    def __str__(self):
        """Mandataire reprensentation."""
        return "Raison social: %s" % (self.raison_social)


class RealEstateUsers(models.Model):
    """Mandataire users."""

    MASTER = "MASTER"
    USER = "USER"
    USER_PROFIL = ((MASTER, "MASTER"), (USER, "USER"))
    societe = models.ForeignKey(
        "RealEstate",
        related_name="societe_users",
        on_delete=models.SET_NULL,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="societe_users",
        on_delete=models.SET_NULL,
        null=True,
    )
    profil = models.CharField(max_length=64, choices=USER_PROFIL, default=USER)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        """Mandataire user representation."""
        return self.societe.raison_social + " " + self.user.email


class Mandat(models.Model):
    """Mandat model."""

    reference_mandat = models.CharField(max_length=150, null=True)
    date_debut = models.DateField(null=False)
    duree = models.IntegerField(null=False, default=12)
    date_echeance = models.DateField()
    tacite_reconduction = models.BooleanField(default=False)
    taux_commission = models.IntegerField(default=10, null=False)
    mandant_physique = models.FileField(upload_to="documents/", null=True)
    immeuble = models.ForeignKey(
        "immeuble.Immeuble", null=True, on_delete=models.SET_NULL
    )
    societe = models.ForeignKey("RealEstate", null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="mandat_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="mandat_updated_user",
    )
