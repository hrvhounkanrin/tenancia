# -*- coding: UTF-8 -*-
"""Contrat models."""
from django.db import models


class Accesoireloyer(models.Model):
    """Accessoireloyer model."""

    libelle = models.CharField(max_length=50)
    utilite = models.CharField(max_length=256)


class Contrat(models.Model):
    """Contrat model."""

    ANNULE = 'ANNULE'
    PROPOSITION = 'PROPOSITION'
    EN_COURS = 'EN COURS'
    RESILIE = 'RESILIE'
    TERME = 'TERME'
    STATUT_CONTRAT = (
        (ANNULE, 'ANNULE'),
        (PROPOSITION, 'PROPOSITION'),
        (EN_COURS, 'EN COURS'),
        (RESILIE, 'RESILIE'),
        (TERME, 'TERME'),
    )
    reference_bail = models.CharField(max_length=50, null=False)
    date_signature = models.DateField(null=False)
    date_effet = models.DateField(null=False)
    periodicite = models.IntegerField()
    duree = models.IntegerField()
    montant_bail = models.DecimalField(
        max_digits=19, decimal_places=10, default=0)
    statut = models.CharField(max_length=64,
                              choices=STATUT_CONTRAT, default=PROPOSITION)
    observation = models.CharField(max_length=256, null=True)
    tacite_reconduction = models.BooleanField(default=True)
    client = models.ForeignKey('client.Client',
                               on_delete=models.CASCADE, null=True,)
    appartement = models.ForeignKey(
        'appartement.Appartement', on_delete=models.CASCADE, null=True,)
    accessoires = models.ManyToManyField(
        Accesoireloyer, through='ContratAccessoiresloyer',
        related_name='accessoires', blank=False)
    mandat = models.ForeignKey('societe.Mandat',
                               null=True, on_delete=models.SET_NULL)


class ContratAccessoiresloyer(models.Model):
    """ContratAccessoiresloyer model."""

    contrat = models.ForeignKey('Contrat', related_name='contrat',
                                on_delete=models.SET_NULL, null=True)
    accesoireloyer = models.ForeignKey(
        'Accesoireloyer', related_name='accesoireloyer',
        on_delete=models.SET_NULL, null=True)
    montant = models.DecimalField(max_digits=19,
                                  decimal_places=10, default=0)
    is_peridic = models.BooleanField(default=False)
    devise = models.CharField(max_length=256, null=False, default='XOF')
    statut = models.CharField(max_length=256, null=False, default='NON PAYE')
    description = models.CharField(max_length=256)
