from django.db import models
from model_utils import Choices
from .baseModel import BaseModel
from .proprietaire import Proprietaire

class Immeuble(BaseModel):
    intitule=models.CharField(max_length=50)
    description=models.CharField(max_length=512, null=True,)
    adresse=models.CharField(max_length=512, null=True,)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, null=False)
    jour_emission_facture=models.IntegerField(default=5)
    jour_valeur_facture=models.IntegerField(default=5)    
    ville=models.CharField(max_length=128,null=True)
    quartier=models.CharField(max_length=128,null=True)
    """Numéro d'identification donné par la mairie ou les autorités locales"""
    ref_immeuble=models.CharField(max_length=50,null=True)
    def __str__(self):
        return '%s %s' % (self.intitule, self.proprietaire.profile.prenom)
