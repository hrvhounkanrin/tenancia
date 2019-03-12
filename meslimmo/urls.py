"""meslimmo URL Configuration

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
app_name ='rest_graph_ql'

from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
#from customuser.views import CreateUSerApiView
urlpatterns = [
    #path(r'^proprio/', include('proprietaire.urls')),
    #path(r'', include('immeuble.urls')),
    #path(r'^contrat/', include('contrat.urls')),
    #path(r'^api/societe/', include('societe.urls')),
    # url(r'^api', include(('appartement.urls' , 'appartement'))),
    url(r'^api/', include(('rest_graph_ql.urls','restapi'))),
    #path(r'^user', include('customuser.urls')),
    url(r'^admin/', admin.site.urls),
]
