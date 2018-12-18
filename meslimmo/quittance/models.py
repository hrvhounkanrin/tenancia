from django.db import models

class Quittance():
    ANNULLEE='ANNULLEE'
    EN_ATTENTE_REGLEMENT='EN ATTENTE DE REGLEMENT'
    REGLEE='REGLEE'
    RETARD_REGLEMENT='EN RETARD DE REGLEMENT'
    STATUT_QUITTANCE = (
                        (ANNULLEE, 'ANNULEE'),
                        (EN_ATTENTE_REGLEMENT, 'EN ATTENTE DE REGLEMENT'),
                        (REGLEE, 'REGLEE'),
                        (RETARD_REGLEMENT, 'RETARD DE REGLEMENT')
                    )
    reference=models.CharField(max_length=20, null=False)
    date_emission=models.DateField()
    date_valeur=models.DateField()
    debut_periode=models.DateField()
    fin_periode=models.DateField()
    nature=models.CharField(max_length=50, null=False)
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUT_QUITTANCE, default=EN_ATTENTE_REGLEMENT)
    date_statut=models.DateField()
    contrat=models.ForeignKey('contrat.Contrat',on_delete=models.SET_NULL,null=True,)
    motif_annulation=models.CharField(max_length=256, null=True)

    def __str__(self):
        return '%s %s' %(self.reference, self.contrat.reference_bail)
