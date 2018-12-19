from django.urls import path

from . import views

urlpatterns = [
    path('get_proprio', views.index, name='index'),
]