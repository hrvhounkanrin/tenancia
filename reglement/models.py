"""Reglement app models."""
from django.db import models


class Reglement(models.Model):
    """Reglement model."""

    STATUT_REGLEMENT = (
        (0, "ANNULE"),
        (1, "REGLE"),
    )
    reference = models.CharField(max_length=50, null=False)
    date_reglement = models.DateField()
    date_valeur = models.DateField()
    montant = models.DecimalField(max_digits=6, decimal_places=2)
    statut = models.IntegerField(choices=STATUT_REGLEMENT, default=1)
    date_statut = models.DateField()
    regle_par = models.CharField(max_length=100, null=False)
    num_telephone = models.CharField(max_length=50, null=False)
    mode_reglement = models.CharField(max_length=100, null=False)
    reference_transaction = models.CharField(max_length=50, null=False)
    quittance = models.ForeignKey(
        "quittance.Quittance",
        on_delete=models.SET_NULL,
        null=True,
    )

    def __init__(self, arg):
        """Reglement str representation."""
        super().__init__()
        self.arg = arg

    def __str__(self):
        """Reglement str representation."""
        return f"{self.reference} {self.regle_par}"
