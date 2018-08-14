from django.db import models
from model_utils import Choices
from .baseModel import BaseModel
from django.conf import settings

class Client(BaseModel):
    """In case of an emergency"""
    ice=models.CharField(max_length=100, null=True)
    ice_number=models.CharField(max_length=50, null=True)
    ice_relation=models.CharField(max_length=100, null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,)

    def __str__(self):
        return '%s %s' % (self.profile.nom, self.profile.prenom)