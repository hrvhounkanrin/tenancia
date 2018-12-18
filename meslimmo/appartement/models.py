from django.db import models

"""
Cette classe sert à gérer une liste dynamiques
des différentes pièces possibles d'un appartement
"""

#All the models must inherit the base  models.Model class


class ComposantAppartement(models.Model):
    libelle = models.CharField(max_length=50)
    utilite = models.CharField(max_length=256)


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
    immeuble = models.ForeignKey('immeuble.Immeuble', null=True, on_delete=models.SET_NULL)
    structure = models.ManyToManyField(ComposantAppartement, through="StructureAppartement",
                                       related_name="structure", blank=False)
    statut = models.CharField(max_length=50, choices=STATUT_APPARTEMENT, default="LIBRE")

    def __str__(self):
        return "Immeuble: intitule {0}".format(self.intitule, )


"""
Cette classe contient la liste des pièces d'un appartement
"""
class StructureAppartement(models.Model):
    appartement= models.ForeignKey('Appartement', related_name='structure_appartement', on_delete=models.SET_NULL, null=True)
    composant=models.ForeignKey('ComposantAppartement', related_name='structure_appartement', on_delete=models.SET_NULL,null=True)
    nbre=models.IntegerField(default=1)
    description=models.CharField(max_length=256)

