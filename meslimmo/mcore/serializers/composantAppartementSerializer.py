from rest_framework import serializers
from mcore.models import ComposantAppartement

class  ComposantAppartementSerializer(serializers.ModelSerializer):

    class Meta:
        model=ComposantAppartement
        fields = '__all__'