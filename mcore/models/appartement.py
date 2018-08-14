from django.db import models
from model_utils import Choices
from .baseModel import BaseModel

class Appartement(BaseModel):
    intitule=models.CharField(max_length=50)
    nb_sejour=models.IntegerField(null=True,)
    nb_chambre=models.IntegerField(null=True,)
    nb_salle_a_manger=models.IntegerField(null=True,)
    nb_cuisine=models.IntegerField(null=True,)
    nb_douche=models.IntegerField(null=True,)
    autre_description=models.TextField(max_length=1024)
    immeuble=models.ForeignKey('Immeuble', on_delete=models.CASCADE,null=False)
    def __unicode__(self):
        return "Immeuble: intitule {0}".format(self.intitule,)
