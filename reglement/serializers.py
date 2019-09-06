"""Reglement app serializer."""
from rest_framework import serializers

from . models import Reglement


class ReglementSerializer(serializers.ModelSerializer):
    """Reglement serializer."""

    class Meta:
        """Reglegement model meta."""

        mode = Reglement
        fields = '__all__'
