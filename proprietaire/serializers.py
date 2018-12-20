from rest_framework import serializers , exceptions

from . models import *

class ProprietaireSerializers(serializers.ModelSerializer):
    """
       Serializer for class proprietaire
    """
    class Meta:
        model = Proprietaire
        fields = '__all__'