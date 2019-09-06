"""Tenancia url place."""
from django.conf.urls import include, url
from rest_framework import routers


router = routers.DefaultRouter()
router.include_root_view = False

urlpatterns = [
    url(r'^clients/', include('client.urls', namespace='clients')),
    url(r'^v1/', include('rest_graph_ql.urls_v1')),
]

urlpatterns += router.urls
