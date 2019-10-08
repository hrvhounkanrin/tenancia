# -*- coding: UTF-8 -*-
"""Proprietaire app models."""
from django.conf import settings
from countries_plus.models import Country
from django.db import models


class Proprietaire(models.Model):
    """Proprietaire model."""

    mode_paiement = models.CharField(max_length=50, null=False)
    numcompte = models.CharField(max_length=50, null=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, )
    banque = models.ForeignKey(
        'banque.Banque', on_delete=models.SET_NULL, null=True, )
    pays_residence = models.ForeignKey(
        Country, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name='proprietaire_created_user')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name='proprietaire_updated_user')

    def _str__(self):
        """Proprietaire str representation."""
        return '%s %s' % (self.user.first_name, self.user.last_name)
