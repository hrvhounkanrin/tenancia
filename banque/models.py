# -*- coding: UTF-8 -*-
"""Banque app models."""
from countries_plus.models import Country
from django.db import models


class Banque(models.Model):
    """Banque model."""

    codebanque = models.CharField(max_length=25, unique=True)
    libbanque = models.CharField(max_length=100)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """Banque model representation."""
        return self.libbanque
