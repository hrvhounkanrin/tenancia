from django.conf import settings
from django.db import models
from model_utils import Choices

class BaseModel(models.Model):
    time_created = models.DateTimeField(auto_now_add=True)
    time_modified = models.DateTimeField(auto_now=True)
    last_modified_by = models.CharField(max_length=100)

    class Meta:
        abstract=True


class Banque(BaseModel):
    codebanque=models.CharField(max_length=25)
    libbanque=models.CharField(max_length=100)

class Proprietaire(BaseModel):
    mode_paiement=models.CharField(max_length=50, null=False)
    numcompte=models.CharField(max_length=50, null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,)
    banque=models.ForeignKey('banque',on_delete=models.CASCADE,null=True,)
    def __str___(self):
        return str(self.profile.nom)

class Immeuble(BaseModel):
    intitule=models.CharField(max_length=50)
    description=models.CharField(max_length=512, null=True,)
    adresse=models.CharField(max_length=512, null=True,)
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE, null=False)
    jour_emission_facture=models.IntegerField(default=5)
    jour_valeur_facture=models.IntegerField(default=5)    
    ville=models.CharField(max_length=128,null=True)
    quartier=models.CharField(max_length=128,null=True)
    """Numéro d'identification donné par la mairie ou les autorités locales"""
    ref_immeuble=models.CharField(max_length=50,null=True)
    def __str__(self):
        return '%s %s' % (self.intitule, self.proprietaire.profile.prenom)


class Appartement(BaseModel):
    intitule=models.CharField(max_length=50)
    nb_sejour=models.IntegerField(null=True,)
    nb_chambre=models.IntegerField(null=True,)
    nb_salle_a_manger=models.IntegerField(null=True,)
    nb_cuisine=models.IntegerField(null=True,)
    nb_douche=models.IntegerField(null=True,)
    autre_description=models.TextField(max_length=1024)
    immeuble=models.ForeignKey('Immeuble', on_delete=models.CASCADE,null=False)
    def __unicode__(self):
        return "Immeuble: intitule {0}".format(self.intitule,)


class Client(BaseModel):
    """In case of an emergency"""
    ice=models.CharField(max_length=100, null=True)
    ice_number=models.CharField(max_length=50, null=True)
    ice_relation=models.CharField(max_length=100, null=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,null=True,)

    def __str__(self):
        return '%s %s' % (self.profile.nom, self.profile.prenom)

class Contrat(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'proposition', ('PROPOSITION')),
                        (2, 'encours', ('EN COURS')),
                        (3, 'resilie', ('RESILIE')),
                        (4, 'terme', ('TERME')),
                     )
    reference_bail=models.CharField(max_length=50, null=False)
    date_signature=models.DateField(null=False)
    date_effet=models.DateField(null=False)
    duree=models.IntegerField()
    periodicite=models.IntegerField()
    montant_bail=models.IntegerField()
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.proposition)
    caution=models.IntegerField()
    caution_eau=models.IntegerField()
    caution_electricite=models.IntegerField()
    observation=models.CharField(max_length=256, null=True)
    client=models.ForeignKey('client',on_delete=models.CASCADE,null=True,)
    appartement=models.ForeignKey('appartement',on_delete=models.CASCADE,null=True,)

    """docstring for Contrat."""
    def __init__(self, arg):
        super(Contrat, self).__init__()
        self.arg = arg

class Facture(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'attente_reglement', ('EN ATTENTE DE REGLEMENT')),
                        (2, 'regle', ('REGLEE')),
                        (3, 'retard_reglement', ('RETARD DE REGLEMENT'))
                    )
    reference=models.CharField(max_length=20, null=False)
    date_emission=models.DateField()
    date_valeur=models.DateField()
    debut_periode=models.DateField()
    fin_periode=models.DateField()
    nature=models.CharField(max_length=50, null=False)
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.attente_reglement)
    date_statut=models.DateField()
    contrat=models.ForeignKey('contrat',on_delete=models.CASCADE,null=True,)

    def __init__(self, arg):
        super(Facture, self).__init__()
        self.arg = arg
    def __str__(self):
        return '%s %s' %(self.reference, self.contrat.reference_bail)


class Reglement(BaseModel):
    STATUTS = Choices(
                        (0, 'annule', ('ANNULE')),
                        (1, 'regle', ('REGLE')),
                     )
    reference=models.CharField(max_length=50, null=False)
    date_reglement=models.DateField()
    date_valeur=models.DateField()
    montant=models.DecimalField(max_digits=6, decimal_places=2)
    statut=models.IntegerField(choices=STATUTS, default=STATUTS.regle)
    date_statut=models.DateField()
    regle_par=models.CharField(max_length=100, null=False)
    num_telephone=models.CharField(max_length=50, null=False)
    mode_reglement=models.CharField(max_length=100, null=False)
    reference_transaction=models.CharField(max_length=50, null=False)
    facture=models.ForeignKey('facture',on_delete=models.CASCADE,null=True,)

    """docstring for Reglement."""
    def __init__(self, arg):
        super(Reglement, self).__init__()
        self.arg = arg

    def __str__(self):
        return '%s %s' %(self.reference, self.regle_par)




