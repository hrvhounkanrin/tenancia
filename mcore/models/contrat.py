from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Contrat(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'proposition', ('PROPOSITION')),
                        (2, 'encours', ('EN COURS')),
                        (3, 'resilie', ('RESILIE')),
                        (4, 'terme', ('TERME')),
                     )
    reference_bail=models.CharField(max_length=50, null=False)
    date_signature=models.DateField(null=False)
    date_effet=models.DateField(null=False)
    duree=models.IntegerField()
    periodicite=models.IntegerField()
    montant_bail=models.IntegerField()
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.proposition)
    caution_loyer=models.IntegerField()
    caution_eau=models.IntegerField()
    caution_electricite=models.IntegerField()
    observation=models.CharField(max_length=256, null=True)
    client=models.ForeignKey('client',on_delete=models.CASCADE,null=True,)
    appartement=models.ForeignKey('appartement',on_delete=models.CASCADE,null=True,)

    """docstring for Contrat."""
    def __init__(self, arg):
        super(Contrat, self).__init__()
        self.arg = arg