from django.db import models
from .baseModel import BaseModel
from django.conf import settings

class Societe(BaseModel):
    raison_social=models.CharField(max_length=150, null=False)
    num_telephone=models.CharField(max_length=50, null=False)
    adresse=models.CharField(max_length=150, null=True)
    logo=models.CharField(max_length=150)
    users=models.ManyToManyField(settings.AUTH_USER_MODEL, through="SocieteUsers",
         related_name="users", blank=True)
    def __str__(self):
        return 'Raison social: %s'%(self.raison_social)
