from django.db import models
from .baseModel import BaseModel
#from .appartement import Appartement
from .composantAppartement import ComposantAppartement


"""
Cette classe contient la liste des pièces d'une appartement
"""
class StructureAppartement(BaseModel):
    appartement= models.ForeignKey('Appartement', related_name='structure_appartement', on_delete=models.SET_NULL, null=True)
    composant=models.ForeignKey('ComposantAppartement', related_name='structure_appartement', on_delete=models.SET_NULL,null=True)
    nbre=models.IntegerField(default=1)
    description=models.CharField(max_length=256)
