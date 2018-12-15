from django.db import models
from .baseModel import BaseModel

"""
Cette classe sert à gérer une liste dynamiques
des différentes pièces possibles d'un appartement
"""
class ComposantAppartement(BaseModel):
    libelle=models.CharField(max_length=50)
    utilite=models.CharField(max_length=256)