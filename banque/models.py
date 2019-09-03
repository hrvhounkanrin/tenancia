"""Banque Models."""
from countries_plus.models import Country
from django.db import models


class Banque(models.Model):
    """Banquea viewsets."""

    codebanque = models.CharField(max_length=25, unique=True)
    libbanque = models.CharField(max_length=100)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        """String.:return."""
        return self.libbanque
