"""Quittance app serializer."""
from rest_framework import serializers

from . models import Quittance


class QuittanceSerializers(serializers.ModelSerializer):
    """Quittance Serializers."""

    class Meta:
        """Quittance serializer meta."""

        model = Quittance
        fields = '__all__'
