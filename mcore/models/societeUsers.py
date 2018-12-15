from django.db import models
from .baseModel import BaseModel
from .societe import Societe
from .django.conf import settings

"""
Cette classe contient la liste des utilisateur d'une agence immobilière
May be on peut gérer ça par les groupes de django, je vais regarder après
"""
class SocieteUsers(BaseModel):
    societe= models.Foreignkey('Societe', related_name='societe_users', on_delete=models.SET_NULL, null=True)
    user=models.Foreignkey(settings.AUTH_USER_MODEL, related_name='societe_users', on_delete=models.SET_NULL,null=True)

