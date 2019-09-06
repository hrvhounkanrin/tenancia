# -*- coding: UTF-8 -*-
"""Housing admin."""
from django.contrib import admin

from . models import Appartement


class AppartementAdmin(admin.ModelAdmin):
    """AppartementAdmin class."""

    list_display = ['id', 'intitule', 'level',
                    'immeuble', 'structure', 'statut']


admin.register(Appartement)
