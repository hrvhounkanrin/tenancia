from django.db import models

#pip install jsfieldsignature
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
    reference_bail=models.CharField(max_length=50, null=False)
    date_signature=models.DateField(null=False)
    date_effet=models.DateField(null=False)
    periodicite=models.IntegerField()
    """La durée est fonction de la périodicité"""
    duree=models.IntegerField()
    montant_bail=models.IntegerField()
    statut=models.CharField(max_length=6, choices=STATUT_CONTRAT, default=PROPOSITION)
    caution_loyer=models.IntegerField()
    caution_eau=models.IntegerField()
    caution_electricite=models.IntegerField()
    observation=models.CharField(max_length=256, null=True)
    tacite_reconduction=models.BooleanField(default=True)
    client=models.ForeignKey('client.Client', on_delete=models.CASCADE, null=True,)
    #https: // docs.djangoproject.com / en / 1.11 / ref / models / fields /  # foreignkey
    appartement=models.ForeignKey('appartement.Appartement', on_delete=models.CASCADE, null=True,)
    #signature field needs to be implemented
