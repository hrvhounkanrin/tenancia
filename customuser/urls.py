from django.conf.urls import url
from customuser.views import CreateUSerApiView
from rest_framework import routers
from customuser.viewsets import UserViewSet
from django.conf.urls import url, include

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^auth/', include('rest_auth.urls')),

]