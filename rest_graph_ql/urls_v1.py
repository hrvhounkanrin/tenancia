"""
Ici reposera nos routes pour  nos API V1
"""
from django.conf.urls import include,  url
from rest_framework import routers
import client.viewsets as client_views
router = routers.SimpleRouter()
# router.register(r'clients',client_views.ClientViewSet )

urlpatterns = [
    url(r'^list_client$', client_views.ClientViewSet.as_view({'get': 'list'}), name='client'),
    # url(r'^auth/logout/$', customer_views.LogoutView.as_view(), name='logout')

]

urlpatterns += router.urls