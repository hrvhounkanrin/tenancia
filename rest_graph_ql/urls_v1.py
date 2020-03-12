"""Tenancia urls v1."""
from django.conf.urls import url
from rest_framework import routers
import banque.viewsets as banque_views
import client.viewsets as client_viewset
import immeuble.viewsets as immeuble_viewsets
import proprietaire.viewsets as proprietaire_viewsets
import quittance.viewsets as quitance_viewsets
from appartement.viewsets \
    import AppartementViewSet as appartement_viewsets
from appartement.viewsets \
    import ComposantAppartementViewSet as component_viewsets
from appartement.viewsets \
    import StructureAppartmentViewSet as structure_viewsets
from contrat.viewsets import AccessoireloyerAction
from contrat.viewsets import ContratAction
from landing import views as landing_view
from societe.viewsets import MandatViewSetAction as mandat_viewset
from societe.viewsets import SocieteViewSetAction as societe_views
from customuser import viewsets as user_views
from customuser.viewsets import AccountViewset
router = routers.SimpleRouter()
urlpatterns = [
    url(r'^$', landing_view.index, name='index'),
    url(r'^banque_action/(?P<action>[^/.]+)',
        banque_views.BanqueViewSet.as_view(), name='banque_action'),
    url(r'^quittance_action/(?P<action>[^/.]+)',
        quitance_viewsets.QuittanceActionViewSet.as_view(),
        name='quittance_action'),
    url(r'^proprietaire_action/(?P<action>[^/.]+)',
        proprietaire_viewsets.ProprietairAction.as_view(),
        name='proprietaire_action'),
    url(r'^client_action/(?P<action>[^/.]+)',
        client_viewset.ClientAction.as_view(),
        name='client_action'),
    url(r'^dependency_action/(?P<action>[^/.]+)', component_viewsets.as_view(),
        name='dependency_action'),
    url(r'^logement_action/(?P<action>[^/.]+)', appartement_viewsets.as_view(),
        name='logement_action'),
    url(r'^structure_action/(?P<action>[^/.]+)', structure_viewsets.as_view(),
        name='structure_action'),
    url(r'^immeuble_action/(?P<action>[^/.]+)',
        immeuble_viewsets.ImmeubleAction.as_view(),
        name='immeuble_action'),
    url(r'^accessoire_action/(?P<action>[^/.]+)',
        AccessoireloyerAction.as_view(),
        name='accessoire_action'),
    url(r'^contrat_action/(?P<action>[^/.]+)', ContratAction.as_view(),
        name='contrat_action'),
    url(r'^mandataire_action/(?P<action>[^/.]+)', societe_views.as_view(),
        name='mandataire_action'),
    url(r'^mandat_action/(?P<action>[^/.]+)', mandat_viewset.as_view(),
        name='mandat_action'),
    url(r'^users$', user_views.UserViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='user_api'),
    url(r'^users/activate$', AccountViewset.as_view(
        {'get': 'activate_account'}), name='account-activate'),

]
urlpatterns += router.urls
