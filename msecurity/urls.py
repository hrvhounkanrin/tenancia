from django.conf.urls import url
from .views import (LoginAPIView, RegistrationAPIView,UserRetrieveUpdateAPIView, ObtainJWTView)
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)

urlpatterns = [
    url(r'^login/', ObtainJWTView.as_view(), name='login'),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^register/?$', RegistrationAPIView.as_view()),
]
