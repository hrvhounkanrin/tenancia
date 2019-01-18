from django.conf.urls import url
from customuser.views import CreateUSerApiView
urlpatterns = [
    url(r'^create/$', CreateUSerApiView.as_view()),
]