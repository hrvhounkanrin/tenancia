from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Reglement(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'regle', ('REGLE')),
                     )
    reference=models.CharField(max_length=50, null=False)
    date_reglement=models.DateField()
    date_valeur=models.DateField()
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.regle)
    date_statut=models.DateField()
    regle_par=models.CharField(max_length=100, null=False)
    num_telephone=models.CharField(max_length=50, null=False)
    mode_reglement=models.CharField(max_length=100, null=False)
    reference_transaction=models.CharField(max_length=50, null=False)
    facture=models.ForeignKey('facture',on_delete=models.CASCADE,null=True,)

    """docstring for Reglement."""
    def __init__(self, arg):
        super(Reglement, self).__init__()
        self.arg = arg

    def __str__(self):
        return '%s %s' %(self.reference, self.regle_par)