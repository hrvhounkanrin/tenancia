# -*- coding: UTF-8 -*-
"""Housing admin."""
from django.contrib import admin

from .models import Appartement


# Register your models here.
class AppartmAdmin(admin.ModelAdmin):
    """Appartment admin class."""

    list_display = ['id', 'intitule', 'level',
                    'immeuble', 'structure', 'statut']


admin.register(Appartement)
