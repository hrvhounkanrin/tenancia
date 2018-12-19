from django.db import models

# Create your models here.


class Client(models.Model):
    nom =  models.CharField(max_length=132,)
    prenom = models.CharField(max_length=132)
    addresse = models.CharField(max_length=32)



    #will pass this just to fix the issue of reference key  missing

