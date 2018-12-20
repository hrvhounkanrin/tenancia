from django.conf import settings
from django.conf.urls import include, url
import client.viewsets as client_rest
import proprietaire.viewsets as proprietaire_rest
from rest_framework import routers


router = routers.DefaultRouter()
router.include_root_view = False
router.register(r'client', client_rest.ClientViewSet, base_name='client')


urlpatterns = [
    # url(r'^', include(router.urls)),

    url(r'^clients/', include('client.urls', namespace='clients')),


    url(r'^v1/', include('rest_graph_ql.urls_v1')),
    # url(r'^v2/', include('rest_graph_ql.urls_v2')),
]

urlpatterns += router.urls