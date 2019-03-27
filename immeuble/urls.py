from django.conf.urls import include, url
from rest_framework import routers
from immeuble.viewsets import ImmeubleViewSet

router = routers.DefaultRouter()
#router.register('immeuble',ImmeubleViewSet)
app_name = 'immeuble'
urlpatterns = [
    #url('immeuble', include(router.urls)),

]
