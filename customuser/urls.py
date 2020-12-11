"""Customuser urls."""
from django.urls import path
from .views import exchange_token as SocialAuth
app_name = "customuser"
urlpatterns = [
    path('social/google-oauth2/', SocialAuth.as_view(), name='google_oauth')
]
