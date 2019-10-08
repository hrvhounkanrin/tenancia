"""Quittance app admin.py."""
from django.contrib import admin

from . models import Quittance


class QuittanceAdmin(admin.ModelAdmin):
    """Quittance admin class."""

    pass


admin.site.register(Quittance, QuittanceAdmin)
