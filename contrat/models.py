# -*- coding: UTF-8 -*-
from django.db import models

class Accesoireloyer(models.Model):
    libelle = models.CharField(max_length=50)
    utilite = models.CharField(max_length=256)

# pip install jsfieldsignature
class Contrat(models.Model):
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
    """Référence généré automatiquement"""
    reference_bail = models.CharField(max_length=50, null=False)
    date_signature = models.DateField(null=False)
    date_effet = models.DateField(null=False)
    periodicite = models.IntegerField()
    """La durée est fonction de la périodicité"""
    duree = models.IntegerField()
    montant_bail = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    statut = models.CharField(max_length=64, choices=STATUT_CONTRAT, default=PROPOSITION)
    #caution_loyer = models.IntegerField()
    #caution_eau = models.IntegerField()
    #caution_electricite = models.IntegerField()
    observation = models.CharField(max_length=256, null=True)
    tacite_reconduction = models.BooleanField(default=True)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True, )
    # https: // docs.djangoproject.com / en / 1.11 / ref / models / fields /  # foreignkey
    appartement = models.ForeignKey('appartement.Appartement', on_delete=models.CASCADE, null=True, )
    accessoires = models.ManyToManyField(Accesoireloyer, through="ContratAccessoiresloyer",
                                         related_name="accessoires", blank=False)
    # signature field needs to be implemented



class ContratAccessoiresloyer(models.Model):
    contrat = models.ForeignKey('Contrat', related_name='contrat', on_delete=models.SET_NULL, null=True)
    accesoireloyer = models.ForeignKey('Accesoireloyer', related_name='accesoireloyer', on_delete=models.SET_NULL, null=True)
    montant = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    is_peridic = models.BooleanField(default=False)
    devise = models.CharField(max_length=256, null=False, default='XOF')
    statut = models.CharField(max_length=256, null=False, default='NON PAYE')
    description = models.CharField(max_length=256)
