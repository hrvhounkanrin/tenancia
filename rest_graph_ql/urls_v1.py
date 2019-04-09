"""
Ici reposera nos routes pour  nos API V1
"""
from django.conf.urls import include,  url
from rest_framework import routers
import client.viewsets as client_views
import banque.viewsets as banque_views
import customuser.viewsets as user_views
import proprietaire.viewsets as proprietaire_views
import immeuble.viewsets as immeuble_views
from appartement.viewsets import AppartementViewSet as appartement_views
from appartement.viewsets import ComposantAppartementViewSet as composant_views
from appartement.viewsets import StructureAppartementViewset as structure_views
from societe.viewsets import SocieteViewSet as societe_views

router = routers.SimpleRouter()
# router.register(r'clients',client_views.ClientViewSet )
router.register(r'banques', banque_views.BanqueViewSet)
router.register(r'proprietaires', proprietaire_views.ProprietaireViewSet)
router.register(r'immeubles', immeuble_views.ImmeubleViewSet)
router.register(r'appartements', appartement_views)
router.register(r'composants', composant_views)
router.register(r'structures', structure_views)
router.register(r'societes', societe_views)

urlpatterns = [
    #url(r'^list_client$', client_views.ClientViewSet.as_view({'get': 'list'}), name='client'),
    #url(r'^immeuble$', immeuble_views.ImmeubleViewSet.as_view({'get': 'list', 'post': 'create'}), name='immeuble_list'),
    #url(r'^immeuble/(?P.+)/$', immeuble_views.ImmeubleViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='immeuble_detail'),
    #url(r'^proprietaire', proprietaire_views.ProprietaireViewSet.as_view({'get': 'list', 'post': 'create'}), name='prorietaire_list'),
    #url(r'^proprietaire/<int:pk>', immeuble_views.ImmeubleViewSet.as_view({'get': 'retrieve','put': 'update','patch': 'partial_update','delete': 'destroy'}), name='proprietaire_detail'),
    url(r'^user', user_views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user_api'),
    # url(r'^auth/logout/$', customer_views.LogoutView.as_view(), name='logout')

]

urlpatterns += router.urls