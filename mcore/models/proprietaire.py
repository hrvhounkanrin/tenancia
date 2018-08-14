from django.db import models
from model_utils import Choices
from .baseModel import BaseModel
from django.conf import settings

class Proprietaire(BaseModel):
    mode_paiement=models.CharField(max_length=50, null=False)
    numcompte=models.CharField(max_length=50, null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,)
    banque=models.ForeignKey('banque',on_delete=models.CASCADE,null=True,)
    def __str___(self):
        return str(self.profile.nom)