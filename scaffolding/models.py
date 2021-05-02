# -*- coding: UTF-8 -*-
"""Scaffolding app models."""
from django.conf import settings
from django.db import models

from appartement.models import TypeDependence


class Immeuble(models.Model):
    """Immeuble models."""

    intitule = models.CharField(max_length=50)
    description = models.CharField(max_length=512, null=True, )
    adresse = models.CharField(max_length=512, null=True, )
    jour_emission_facture = models.IntegerField(default=5)
    jour_valeur_facture = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        editable=False, related_name='simmeuble_created_user')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        editable=False, related_name='simmeuble_updated_user')

    def __str__(self):
        """Immeuble representation."""
        return '%s %s' % (self.intitule,)

    class Meta:
        """Immeuble model meta."""

        verbose_name = 'Immeuble'
        verbose_name_plural = 'Immeubles'


class Appartement(models.Model):
    """Appartement model."""

    LIBRE = 'LIBRE'
    RESERVE = 'RESERVE'
    OCCUPE = 'OCCUPE'
    BIENTOT_LIBRE = 'BIENTOT LIBRE'
    STATUT_APPARTEMENT = (
        (LIBRE, 'LIBRE'),
        (RESERVE, 'RESERVE'),
        (OCCUPE, 'OCCUPE'),
        (BIENTOT_LIBRE, 'BIENTOT_LIBRE')
    )
    intitule = models.CharField(max_length=50)
    level = models.IntegerField(null=False)
    autre_description = models.TextField(max_length=1024)
    immeuble = models.ForeignKey('scaffolding.Immeuble',
                                 null=True, on_delete=models.SET_NULL)
    structure = models.ManyToManyField(
        TypeDependence, through='StructureAppartement',
        blank=False, related_name='scaffolding_structure')
    statut = models.CharField(max_length=50,
                              choices=STATUT_APPARTEMENT, default='LIBRE')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        editable=False, related_name='sappartement_created_user')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,
        editable=False, related_name='sappartement_updated_user')

    def __str__(self):
        """Appartement representation."""
        return 'Immeuble: intitule {0}'.format(self.intitule, )


class StructureAppartement(models.Model):
    """StructureAppartement model."""

    appartement = models.ForeignKey(
        'Appartement', related_name='scaffolding_appartement',
        on_delete=models.SET_NULL, null=True)
    composantAppartement = models.ForeignKey(
        'appartement.TypeDependence',
        related_name='scaffolding_composant_appartement',
        on_delete=models.SET_NULL, null=True)
    nbre = models.IntegerField(default=1)
    description = models.CharField(max_length=256)
    is_periodic = models.BooleanField(default=False)
