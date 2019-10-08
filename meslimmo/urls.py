"""Meslimmo URL Configuration."""
from rest_framework_jwt.views import obtain_jwt_token
from django.contrib import admin
from django.conf.urls import include, url
from landing import views as landing_view
"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

admin.autodiscover()
app_name = 'rest_graph_ql'


urlpatterns = [
    url(r'^$', landing_view.index, name='index'),
    url(r'^api/', include(('rest_graph_ql.urls', 'restapi'))),
    url(r'^user_jwt/', obtain_jwt_token),
    url(r'^admin/', admin.site.urls),
]
