"""
Ici reposera nos routes pour  nos API V1
"""
from django.conf.urls import include,  url
from rest_framework import routers
import client.viewsets as client_views
import immeuble.viewsets as immeuble_views
router = routers.SimpleRouter()
# router.register(r'clients',client_views.ClientViewSet )

urlpatterns = [
    url(r'^list_client$', client_views.ClientViewSet.as_view({'get': 'list'}), name='client'),
    url(r'^immeuble$', immeuble_views.ImmeubleViewSet.as_view({'get': 'list', 'post': 'create'}), name='immeuble_list'),
    url(r'^immeuble/(?P<pk>\d+)/$', immeuble_views.ImmeubleViewSet.as_view(
        {'get': 'retrieve', 
        'put': 'update', 
        'patch': 'partial_update', 
        'delete': 'destroy'}), name='immeuble_detail'),

    # url(r'^auth/logout/$', customer_views.LogoutView.as_view(), name='logout')

]

urlpatterns += router.urls