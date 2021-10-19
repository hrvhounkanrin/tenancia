"""Housing app models."""
from django.conf import settings
from django.db import models


class TypeDependence(models.Model):
    """Housing depenency type."""

    libelle = models.CharField(max_length=50)
    utilite = models.CharField(max_length=256, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)


class Appartement(models.Model):
    """Housing model."""

    LIBRE = "LIBRE"
    RESERVE = "RESERVE"
    OCCUPE = "OCCUPE"
    BIENTOT_LIBRE = "BIENTOT LIBRE"

    STATUT_APPARTEMENT = (
        (LIBRE, "LIBRE"),
        (RESERVE, "RESERVE"),
        (OCCUPE, "OCCUPE"),
        (BIENTOT_LIBRE, "BIENTOT_LIBRE"),
    )
    intitule = models.CharField(max_length=50)
    """level le niveau de l'appartement sur l'immeuble."""
    level = models.IntegerField(default=0, null=False)
    autre_description = models.TextField(max_length=1024, null=True)
    immeuble = models.ForeignKey(
        "immeuble.Immeuble", null=True, on_delete=models.SET_NULL
    )
    structure = models.ManyToManyField(
        TypeDependence,
        through="StructureAppartement",
        related_name="structure",
        blank=False,
    )
    statut = models.CharField(
        max_length=50, choices=STATUT_APPARTEMENT, default="LIBRE"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="appartement_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="appartement_updated_user",
    )

    def __str__(self):
        """Housing reprensentation."""
        return f"Immeuble: intitule {self.intitule}"


class StructureAppartement(models.Model):
    """Housing dependencies."""

    appartement = models.ForeignKey(
        "Appartement", related_name="appartement", on_delete=models.SET_NULL, null=True
    )
    typedependence = models.ForeignKey(
        "TypeDependence",
        related_name="appartement_typedependence",
        on_delete=models.SET_NULL,
        null=True,
    )
    nbre = models.IntegerField(default=1)
    superficie = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    description = models.CharField(max_length=256)
    is_periodic = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="structure_created_user",
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        editable=False,
        related_name="structure_updated_user",
    )

    def __str__(self):
        """Housing reprensentation."""
        return f"Dépendence: {self.typedependence.libelle} | {self.nbre}"
