"""
Ici reposera nos routes pour  nos API V1
"""
from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

import banque.viewsets as banque_views
import customuser.viewsets as user_views
import factures.viewsets as factures_viewsets
import immeuble.viewsets as immeuble_views
import proprietaire.viewsets as proprietaire_viewsets
import quittance.viewsets as quitance_viewsets
from appartement.viewsets import AppartementViewSet as appartement_views
from appartement.viewsets import ComposantAppartementViewSet as composant_views
from appartement.viewsets import StructureAppartementViewset as structure_views
from client.viewsets import ClientViewSet as client_view
from contrat.viewsets import AccessoireloyerViewSet as accessoires_view
from contrat.viewsets import ContratAccessoiresloyerViewSet as contrat_acccessoires_view
from contrat.viewsets import ContratViewSet as contrat_view
from landing import views as landing_view
from societe.viewsets import SocieteViewSet as societe_views
router = routers.SimpleRouter()
router.register(r'banques', banque_views.BanqueViewSet)
router.register(r'proprietaires', proprietaire_viewsets.ProprietaireViewSet)
router.register(r'clients', client_view)
router.register(r'immeubles', immeuble_views.ImmeubleViewSet)
router.register(r'appartements', appartement_views)
router.register(r'composants', composant_views)
router.register(r'structures', structure_views)
router.register(r'societes', societe_views)
router.register(r'contrats', contrat_view)
router.register(r'accessoires', accessoires_view)
router.register(r'contrataccessoires', contrat_acccessoires_view)

urlpatterns = [
    url(r'^/$', landing_view.index, name='index'),
    url(r'^$', landing_view.index, name='index'),
    url(r'^user', user_views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_api'),
    url(r'^quittance_action/(?P<action>[^/.]+)', quitance_viewsets.QuittanceActionViewSet.as_view(), name='quittance_action'),
    url(r'^invoicing_action/(?P<action>[^/.]+)',  factures_viewsets.InvoicingActionViewSet.as_view(), name='facture_action'),
    url(r'^proprietaire_action/(?P<action>[^/.]+)', proprietaire_viewsets.ProprietairAction.as_view(),
        name='quittance_action'),

]

urlpatterns += router.urls
