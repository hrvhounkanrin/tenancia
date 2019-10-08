# -*- coding: UTF-8 -*-
"""Banque app serializer."""
from rest_framework import serializers

from .models import Banque


class BanqueSerializers(serializers.ModelSerializer):
    """Banque Model serializer."""

    class Meta:
        """Banque model meta."""

        model = Banque
        fields = '__all__'
        extra_kwargs = {
            'codebanque': {'validators': []},
        }
