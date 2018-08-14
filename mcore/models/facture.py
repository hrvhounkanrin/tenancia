from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Facture(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'attente_reglement', ('EN ATTENTE DE REGLEMENT')),
                        (2, 'regle', ('REGLEE')),
                        (3, 'retard_reglement', ('RETARD DE REGLEMENT'))
                    )
    reference=models.CharField(max_length=20, null=False)
    date_emission=models.DateField()
    date_valeur=models.DateField()
    debut_periode=models.DateField()
    fin_periode=models.DateField()
    nature=models.CharField(max_length=50, null=False)
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.attente_reglement)
    date_statut=models.DateField()
    contrat=models.ForeignKey('contrat',on_delete=models.CASCADE,null=True,)

    def __init__(self, arg):
        super(Facture, self).__init__()
        self.arg = arg
    def __str__(self):
        return '%s %s' %(self.reference, self.contrat.reference_bail)
