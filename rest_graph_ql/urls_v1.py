"""Tenancia urls v1."""
from django.conf.urls import url
from django.urls import re_path, path

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
from customuser.views import PasswordResetView
from rest_auth.views import PasswordResetConfirmView
from rest_auth.registration.views import RegisterView, VerifyEmailView
from allauth.account.views import ConfirmEmailView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.SimpleRouter()
urlpatterns = [
    url(r'^$', landing_view.index, name='index'),
    url(r'^banque_action/(?P<action>[^/.]+)$',
        banque_views.BanqueViewSet.as_view(), name='banque_action'),
    url(r'^quittance_action/(?P<action>[^/.]+)$',
        quitance_viewsets.QuittanceActionViewSet.as_view(),
        name='quittance_action'),
    url(r'^proprietaire_action/(?P<action>[^/.]+)$',
        proprietaire_viewsets.ProprietairAction.as_view(),
        name='proprietaire_action'),
    url(r'^client_action/(?P<action>[^/.]+)$',
        client_viewset.ClientAction.as_view(),
        name='client_action'),
    url(r'^dependency_action/(?P<action>[^/.]+)$', component_viewsets.as_view(),
        name='dependency_action'),
    url(r'^logement_action/(?P<action>[^/.]+)$', appartement_viewsets.as_view(),
        name='logement_action'),
    url(r'^structure_action/(?P<action>[^/.]+)$', structure_viewsets.as_view(),
        name='structure_action'),
    url(r'^immeuble_action/(?P<action>[^/.]+)$',
        immeuble_viewsets.ImmeubleAction.as_view(),
        name='immeuble_action'),
    url(r'^accessoire_action/(?P<action>[^/.]+)$',
        AccessoireloyerAction.as_view(),
        name='accessoire_action'),
    url(r'^contrat_action/(?P<action>[^/.]+)$', ContratAction.as_view(),
        name='contrat_action'),
    url(r'^mandataire_action/(?P<action>[^/.]+)$', societe_views.as_view(),
        name='mandataire_action'),
    url(r'^mandat_action/(?P<action>[^/.]+)$', mandat_viewset.as_view(),
        name='mandat_action'),
    url(r'^users$', user_views.UserViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='user_api'),
    url(r'^users/activate$', AccountViewset.as_view(
        {'get': 'activate_account'}), name='account-activate'),
    url(r'^password/reset/$', PasswordResetView.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirmView.as_view(),
        name='rest_password_reset_confirm'),

    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(),
        name='account_confirm_email'),
    url(r'^users/register/$', RegisterView.as_view(), name='rest_register'),

    # path('registration/', RegisterView.as_view(), name='account_signup'),
    re_path(r'^account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', VerifyEmailView.as_view(),
         name='account_confirm_email'),
]

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns_swagger = [
   url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += urlpatterns_swagger
urlpatterns += router.urls
