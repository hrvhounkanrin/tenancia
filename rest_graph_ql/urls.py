from django.conf import settings
from django.conf.urls import include, url
import client.viewsets as client_rest
from rest_framework import routers


router = routers.DefaultRouter()
router.include_root_view = False

urlpatterns = [
    # url(r'^', include(router.urls)),

    url(r'^clients/', include('client.urls', namespace='clients')),


    url(r'^v1/', include('rest_graph_ql.urls_v1')),
    # url(r'^v2/', include('rest_graph_ql.urls_v2')),
    # url(r'^end_point_/(?P<action>[^/.]+)', app_view_name.ClassBaseViewSet.as_view(),name='aactioon')  #example of root endpoint definition,
]

urlpatterns += router.urls