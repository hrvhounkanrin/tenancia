# -*- coding: UTF-8 -*-
"""Immeuble admin.py."""
from django.contrib import admin

from . models import Immeuble


class ImmeubleAdmin(admin.ModelAdmin):
    """Immeuble admin class."""

    save_on_top = True
    list_display = ['id', 'intitule', 'description',
                    'adresse', 'proprietaire', 'jour_emission_facture',
                    'jour_valeur_facture', 'ville', 'quartier',
                    'pays', 'longitude', 'latitude', 'ref_immeuble']
    list_display_links = 'id'


admin.site.register(Immeuble)
