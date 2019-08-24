# -*- coding: UTF-8 -*-
from django.conf.urls import include, url
from rest_framework import routers
from societe.viewsets import SocieteViewSet

router = routers.DefaultRouter()
router.register(r'societe', SocieteViewSet, base_name='societe')
app_name = 'societe'
urlpatterns = [
    url(r'api/societe', include(router.urls)),

]
