from django.db import models
from .baseModel import BaseModel
from .composantAppartement import ComposantAppartement
from .appartement import Appartement

"""
Cette classe contient la liste des pièces d'une appartement
"""
class StructureAppartement(BaseModel):
    appartement= models.Foreignkey('Appartement', related_name='structure_appartement', on_delete=models.SET_NULL, null=True)
    composant=models.Foreignkey('ComposantAppartement', related_name='structure_appartement', on_delete=models.SET_NULL,null=True)
    nbre=models.IntegerField(default=1)
    description=models.CharField(max_length=256)
