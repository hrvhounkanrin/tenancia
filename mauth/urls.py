from django.conf.urls import url
#from django.urls import include, path, 
from .views import (LoginAPIView, RegistrationAPIView,UserRetrieveUpdateAPIView,)
from rest_framework_jwt.views import (obtain_jwt_token, refresh_jwt_token, verify_jwt_token)

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    url(r'^login/', LoginAPIView.as_view(), name='login'),
    url(r'^user/?$', UserRetrieveUpdateAPIView.as_view()),
    url(r'^register/?$', RegistrationAPIView.as_view()),

]
