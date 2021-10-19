"""Contrat models."""
from django.conf import settings
from django.db import models


class Accesoireloyer(models.Model):
    """Accessoireloyer model."""

    libelle = models.CharField(max_length=50)
    utilite = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)


class Contrat(models.Model):
    """Contrat model."""

    ANNULE = "ANNULE"
    PROPOSITION = "PROPOSITION"
    ACCORD_CLIENT = "CONTRAT ACCEPTE"
    EN_COURS = "EN COURS"
    RESILIE = "RESILIE"
    TERME = "TERME"
    STATUT_CONTRAT = (
        (ANNULE, "ANNULE"),
        (PROPOSITION, "PROPOSITION"),
        (EN_COURS, "EN COURS"),
        (RESILIE, "RESILIE"),
        (TERME, "TERME"),
    )
    MENSUELLE = 12
    TRIMESTRIELLE = 4
    SEMESTRIELLE = 2
    ANNUELLE = 1
    PERIODICITE_CONTRAT = (
        (MENSUELLE, "MENSUELLE"),
        (TRIMESTRIELLE, "TRIMESTRIELLE"),
        (SEMESTRIELLE, "SEMESTRIELLE"),
        (ANNUELLE, "ANNUELLE")
    )
    reference_bail = models.CharField(max_length=50, null=False)
    date_signature = models.DateField(null=False)
    date_effet = models.DateField(null=False)
    periodicite = models.IntegerField(choices=PERIODICITE_CONTRAT, default=MENSUELLE)
    duree = models.IntegerField(default=0)
    montant_bail = models.DecimalField(max_digits=9, decimal_places=2)
    nb_avance = models.IntegerField(default=0)
    nb_prepaye = models.IntegerField(default=0)
    statut = models.CharField(
        max_length=64, choices=STATUT_CONTRAT, default=PROPOSITION
    )
    observation = models.CharField(max_length=256, null=True)
    tacite_reconduction = models.BooleanField(default=True)
    client = models.ForeignKey(
        "client.Client",
        on_delete=models.CASCADE,
        null=True,
    )
    appartement = models.ForeignKey(
        "appartement.Appartement",
        on_delete=models.CASCADE,
        null=True,
    )
    accessoires = models.ManyToManyField(
        Accesoireloyer,
        through="ContratAccessoiresloyer",
        related_name="accessoires",
        blank=False,
    )
    mandat = models.ForeignKey("societe.Mandat", null=True, on_delete=models.SET_NULL)
    prochaine_echeance = models.DateField(null=True)

    jour_emission = models.IntegerField(null=False, default=5)
    client_accord = models.BooleanField(default=False)
    date_accord_client = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contrat_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contrat_updated_user",
    )


class ContratAccessoiresloyer(models.Model):
    """ContratAccessoiresloyer model."""

    contrat = models.ForeignKey(
        "Contrat", related_name="contrat", on_delete=models.SET_NULL, null=True
    )
    accesoireloyer = models.ForeignKey(
        "Accesoireloyer",
        related_name="accesoireloyer",
        on_delete=models.SET_NULL,
        null=True,
    )
    montant = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    is_peridic = models.BooleanField(default=False)
    devise = models.CharField(max_length=256, null=False, default="XOF")
    statut = models.CharField(max_length=256, null=False, default="NON REGLE")
    description = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contrat_accessoire_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="contrat_accessoire_updated_user",
    )
