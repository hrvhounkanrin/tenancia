from django.conf.urls import include, url
from rest_framework import routers
from contrat.viewsets import ContratViewSet

router = routers.DefaultRouter()
router.register(r'contrat', ContratViewSet, base_name='contrat')
app_name = 'contrat'
urlpatterns = [
    url(r'api/contrat', include(router.urls)),

]
