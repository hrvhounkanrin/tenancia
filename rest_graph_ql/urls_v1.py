"""
Ici reposera nos routes pour  nos API V1
"""
from django.conf.urls import include,  url
from rest_framework import routers
import client.viewsets as client_viewset
import banque.viewsets as banque_views
import customuser.viewsets as user_views
import proprietaire.viewsets as proprietaire_viewsets
from appartement.viewsets import ComposantAppartementViewSet as component_viewsets
from appartement.viewsets import AppartementViewSet as appartement_viewsets
from appartement.viewsets import StructureAppartmentViewSet as structure_viewsets
import immeuble.viewsets as immeuble_viewsets
from contrat.viewsets import *
from societe.viewsets import SocieteViewSet as societe_views

from landing import views as landing_view
import quittance.viewsets as quitance_viewsets
router = routers.SimpleRouter()


urlpatterns = [
    url(r'^/$', landing_view.index, name='index'),
    url(r'^$', landing_view.index, name="index"),
    url(r'^user', user_views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_api'),
    url(r'^quittance_action/(?P<action>[^/.]+)', quitance_viewsets.QuittanceActionViewSet.as_view(), name='quittance_action'),
    url(r'^proprietaire_action/(?P<action>[^/.]+)', proprietaire_viewsets.ProprietairAction.as_view(),
        name='quittance_action'),
    url(r'^client_action/(?P<action>[^/.]+)', client_viewset.ClientAction.as_view(),
        name='client_action'),
    url(r'^component_action/(?P<action>[^/.]+)', component_viewsets.as_view(),
        name='component_action'),
    url(r'^appartement_action/(?P<action>[^/.]+)', appartement_viewsets.as_view(),
        name='appartement_action'),
    url(r'^structure_action/(?P<action>[^/.]+)', structure_viewsets.as_view(),
        name='structure_action'),
    url(r'^immeuble_action/(?P<action>[^/.]+)', immeuble_viewsets.ImmeubleAction.as_view(),
        name='immeuble_action'),
    url(r'^accessoire_action/(?P<action>[^/.]+)', AccessoireloyerAction.as_view(),
        name='accessoire_action'),
    url(r'^contrat_action/(?P<action>[^/.]+)', ContratAction.as_view(),
        name='contrat_action'),

    # url(r'^auth/logout/$', customer_views.LogoutView.as_view(), name='logout')

]

urlpatterns += router.urls