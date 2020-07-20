from countries_plus.models import Country
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from tools.serializers import CountrySerialier


class CountryListView(ListAPIView):
    """Return allowed contries"""

    permission_classes = (AllowAny,)
    serializer_class = CountrySerialier
    allowed_country = ['BF', 'BJ', 'CM', 'BJ', 'TG', 'FR', 'NER']
    queryset = Country.objects.filter(iso__in=allowed_country)
