from django.db import models
from .baseModel import BaseModel
from .composantAppartement import ComposantAppartement
from .structureAppartement import StructureAppartement

class Appartement(BaseModel):
    LIBRE="LIBRE"
    RESERVE="RESERVE"
    OCCUPE="OCCUPE"
    BIENTOT_LIBRE="BIENTOT LIBRE"

    STATUT_APPARTEMENT = (
        (LIBRE, 'LIBRE'),
        (RESERVE, 'RESERVE'),
        (OCCUPE, 'OCCUPE'),
        (BIENTOT_LIBRE, 'BIENTOT_LIBRE')
    )
    intitule=models.CharField(max_length=50)
    """level indique le niveau de l'appartement sur l'immeuble: 0 pour le rez de chaussé
         et peut prendre des signes négatifs pour les sous sols"""
    level =models.IntegerField(null=False)
    autre_description=models.TextField(max_length=1024)
    immeuble=models.ForeignKey('Immeuble',null=True, on_delete=models.SET_NULL)
    structure=models.ManyToManyField(ComposantAppartement, through="StructureAppartement",
         related_name="structure", blank=False)
    statut=models.CharField(max_length=50, choices=STATUT_APPARTEMENT, default="LIBRE")

    def __str__(self):
        return "Immeuble: intitule {0}".format(self.intitule,)
