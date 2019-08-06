from django.db import models
from appartement.models import ComposantAppartement

class Immeuble(models.Model):
    intitule = models.CharField(max_length=50)
    description = models.CharField(max_length=512, null=True, )
    adresse = models.CharField(max_length=512, null=True, )
    jour_emission_facture = models.IntegerField(default=5)
    jour_valeur_facture = models.IntegerField(default=5)

    def __str__(self):
        return '%s %s' % (self.intitule,)


    class Meta:
        verbose_name = "Immeuble"
        verbose_name_plural = "Immeubles"



class Appartement(models.Model):
    LIBRE = "LIBRE"
    RESERVE = "RESERVE"
    OCCUPE = "OCCUPE"
    BIENTOT_LIBRE = "BIENTOT LIBRE"

    STATUT_APPARTEMENT = (
        (LIBRE, 'LIBRE'),
        (RESERVE, 'RESERVE'),
        (OCCUPE, 'OCCUPE'),
        (BIENTOT_LIBRE, 'BIENTOT_LIBRE')
    )
    intitule = models.CharField(max_length=50)
    """level indique le niveau de l'appartement sur l'immeuble: 0 pour le rez de chaussé
         et peut prendre des signes négatifs pour les sous sols"""
    level = models.IntegerField(null=False)
    autre_description = models.TextField(max_length=1024)
    immeuble = models.ForeignKey('scaffolding.Immeuble', null=True, on_delete=models.SET_NULL)
    structure = models.ManyToManyField(ComposantAppartement, through="StructureAppartement",
                                       related_name="scaffolding_structure", blank=False)
    statut = models.CharField(max_length=50, choices=STATUT_APPARTEMENT, default="LIBRE")

    def __str__(self):
        return "Immeuble: intitule {0}".format(self.intitule, )


"""
Cette classe contient la liste des pieces d'un appartement
"""
class StructureAppartement(models.Model):
    appartement = models.ForeignKey('Appartement', related_name='scaffolding_appartement', on_delete=models.SET_NULL, null=True)
    composantAppartement = models.ForeignKey('appartement.ComposantAppartement', related_name='scaffolding_composant_appartement', on_delete=models.SET_NULL, null=True)
    nbre = models.IntegerField(default=1)
    description = models.CharField(max_length=256)
    is_periodic = models.BooleanField(default=False)

