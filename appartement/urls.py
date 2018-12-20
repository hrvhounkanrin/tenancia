from django.conf.urls import include, url
from rest_framework import routers
from  appartement import viewsets
router = routers.DefaultRouter()
router.register(r'listappart', viewsets.GetAppartmentViewSet, base_name='appartement')
app_name = 'appartement'
urlpatterns = [
    url(r'get_appart', include(router.urls)),

]