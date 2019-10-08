# -*- coding: UTF-8 -*-
"""Client app models."""
from django.conf import settings
from django.db import models


class Client(models.Model):
    """Client model."""

    mode_paiement = models.CharField(max_length=64, null=True, blank=True)
    profession = models.CharField(max_length=128, null=True, blank=True)
    ice_contact = models.CharField(max_length=128, null=True, blank=False)
    ice_number = models.CharField(max_length=28, null=True, blank=False)
    ice_relation = models.CharField(max_length=64, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE, null=True, )
    banque = models.ForeignKey('banque.Banque',
                               on_delete=models.SET_NULL, null=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name='client_created_user')
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name='client_updated_user')

    def __str__(self):
        """Client representation."""
        return '%s %s' % (self.user.first_name, self.user.last_name)

    # will pass this just to fix the issue of reference key  missing
