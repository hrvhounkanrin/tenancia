"""Societe app admin.py."""
from django.contrib import admin

from .models import Mandat
from .models import Societe


class SocieteAdmin(admin.ModelAdmin):
    """Societe admin class."""

    pass


class MandatAdmin(admin.ModelAdmin):
    """Mandat admin class."""

    pass


admin.site.register(Societe, SocieteAdmin)
admin.site.register(Mandat, MandatAdmin)
