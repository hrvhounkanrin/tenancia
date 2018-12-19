from django.db import models
from countries_plus.models import Country

class Immeuble(models.Model):
    intitule = models.CharField(max_length=50)
    description = models.CharField(max_length=512, null=True, )
    adresse = models.CharField(max_length=512, null=True, )
    proprietaire = models.ForeignKey('proprietaire.Proprietaire', on_delete=models.CASCADE, null=False)
    jour_emission_facture = models.IntegerField(default=5)
    jour_valeur_facture = models.IntegerField(default=5)
    ville = models.CharField(max_length=128, null=True)
    quartier = models.CharField(max_length=128, null=True)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    longitude = models.DecimalField(max_digits=20, decimal_places=12)
    latitude = models.DecimalField(max_digits=20, decimal_places=12)
    """Numéro d'identification donné par la mairie ou les autorités locales"""
    ref_immeuble = models.CharField(max_length=50, null=True)

    def __str__(self):
        return '%s %s' % (self.intitule, self.proprietaire.user.last_name)