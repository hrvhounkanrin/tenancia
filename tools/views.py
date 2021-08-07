"""Misc views."""
import json

import requests
from countries_plus.models import Country
from django.conf import settings
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from tools.serializers import CountrySerialier


# https://medium.com/@pratique/social-login-with-react-and-django-i-c380fe8982e2
class CountryListView(ListAPIView):
    """Return allowed contries."""

    permission_classes = (AllowAny,)
    serializer_class = CountrySerialier
    allowed_country = ["BF", "BJ", "CM", "BJ", "TG", "FR", "NER"]
    queryset = Country.objects.filter(iso__in=allowed_country)
