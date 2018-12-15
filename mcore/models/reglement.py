from django.db import models
from .baseModel import BaseModel

class Reglement(BaseModel):
     STATUT_REGLEMENT = (
        (0, 'ANNULE'),
        (1, 'REGLE'),
    )
    
    """reference de reglement générée automatiquement"""
    reference=models.CharField(max_length=50, null=False)
    date_reglement=models.DateField()
    date_valeur=models.DateField()
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUT_REGLEMENT, default=1)
    date_statut=models.DateField()
    """Nom de la personne qui a réglé la quittance"""
    regle_par=models.CharField(max_length=100, null=False)
    num_telephone=models.CharField(max_length=50, null=False)
    mode_reglement=models.CharField(max_length=100, null=False)
    reference_transaction=models.CharField(max_length=50, null=False)
    quittance=models.ForeignKey('Quittance',on_delete=models.SET_NULL,null=True,)

    """docstring for Reglement."""
    def __init__(self, arg):
        super(Reglement, self).__init__()
        self.arg = arg

    def __str__(self):
        return '%s %s' %(self.reference, self.regle_par)