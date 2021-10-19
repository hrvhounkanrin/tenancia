"""Banque app models."""
from countries_plus.models import Country
from django.conf import settings
from django.db import models


class Banque(models.Model):
    """Banque model."""
    codebanque = models.CharField(max_length=25, unique=True)
    code_swift = models.CharField(max_length=25, unique=True, null=True)
    libbanque = models.CharField(max_length=100)
    is_bank = models.BooleanField(default=True)
    pays = models.ForeignKey(Country, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.IntegerField(null=True)
    modified_by = models.IntegerField(null=True)

    def __str__(self):
        """Banque model representation."""
        return "Code swift: {}, nom banque: {}".format(self.code_swift, self.libbanque)
