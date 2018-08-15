from django.db import models
from model_utils import Choices
from .baseModel import BaseModel
from django.conf import settings

class Proprietaire(BaseModel):
    mode_paiement=models.CharField(max_length=50, null=False)
    numcompte=models.CharField(max_length=50, null=True)
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,)
    banque=models.ForeignKey('banque',on_delete=models.CASCADE,null=True,)
    
    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)