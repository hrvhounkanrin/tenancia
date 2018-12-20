from django.db import models

# Create your models here.


class Client(models.Model):
    nom =  models.CharField(max_length=132, null=True, blank=True)
    prenom = models.CharField(max_length=132, null=True, blank=True)
    addresse = models.CharField(max_length=32, null=True, blank=True)

    def __str__(self):
        return  self.nom



    #will pass this just to fix the issue of reference key  missing

