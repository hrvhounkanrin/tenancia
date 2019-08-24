# -*- coding: UTF-8 -*-
from django.db import models
from django.conf import settings

class Societe(models.Model):
    raison_social = models.CharField(max_length=150, null=False)
    num_telephone = models.CharField(max_length=50, null=False)
    adresse = models.CharField(max_length=150, null=True)
    logo = models.CharField(max_length=150)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through="SocieteUsers",
         related_name="users", blank=True)
    def __str__(self):
        return 'Raison social: %s'%(self.raison_social)



"""
Cette classe contient la liste des utilisateur d'une agence immobilière
May be on peut gérer ça par les groupes de django, je vais regarder après
"""
class SocieteUsers(models.Model):
    societe = models.ForeignKey('Societe', related_name='societe_users', on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='societe_users', on_delete=models.SET_NULL,null=True)

    def __unicode__(self):
        return self.societe.raison_social + " " + self.user.email



