"""Quittance app models."""
from django.conf import settings
from django.db import models


class Quittance(models.Model):
    """Quittance model."""

    ANNULLEE = "ANNULLEE"
    EN_ATTENTE_REGLEMENT = "EN ATTENTE DE REGLEMENT"
    REGLEE = "REGLEE"
    RETARD_REGLEMENT = "EN RETARD DE REGLEMENT"
    STATUT_QUITTANCE = (
        (ANNULLEE, "ANNULEE"),
        (EN_ATTENTE_REGLEMENT, "EN ATTENTE DE REGLEMENT"),
        (REGLEE, "REGLEE"),
        (RETARD_REGLEMENT, "RETARD DE REGLEMENT"),
    )

    reference = models.CharField(max_length=20, null=False)
    date_emission = models.DateField()
    date_valeur = models.DateField()
    debut_periode = models.DateField()
    fin_periode = models.DateField()
    nature = models.CharField(max_length=50, null=False)
    montant = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    statut = models.CharField(
        max_length=64, choices=STATUT_QUITTANCE, default=EN_ATTENTE_REGLEMENT
    )
    date_statut = models.DateField(auto_now_add=True)
    contrat = models.ForeignKey(
        "contrat.Contrat",
        on_delete=models.SET_NULL,
        null=True,
    )
    motif_annulation = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="quittance_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="quittance_updated_user",
    )

    class Meta:
        ordering = (["-created_at", "contrat"],)
        # permissions = [('is_lessor',)]

    def __str__(self):
        """Quittance str reprensentation."""
        return f"{self.reference} {self.contrat.reference_bail}"
