from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from mcore.views import banque_view

router = DefaultRouter()
router.register(r'banque', banque_view.BanqueViewSet)

urlpatterns = router.urls