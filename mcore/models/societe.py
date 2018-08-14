from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Societe(BaseModel):
    raison_social=models.CharField(max_length=150, null=False)
    num_telephone=models.CharField(max_length=50, null=False)
    adresse=models.CharField(max_length=150, null=True)
    logo=models.CharField(max_length=150)

    def __str__(self):
        return 'Raison social: %s'%(self.raison_social)
