"""Customuser urls."""
from django.urls import path
from .viewsets import AccountViewset

app_name = "customuser"
urlpatterns = [
    path(
        "users/activate$",
        AccountViewset.as_view({"get": "activate_account"}),
        name="activate",
    )
]
