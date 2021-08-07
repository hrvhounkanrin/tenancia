"""Banque app admin.py."""
from django.contrib import admin

from .models import Banque


class BanqueAdmin(admin.ModelAdmin):
    """Banque admin class."""

    list_display = ("codebanque", "libbanque", "pays")


admin.site.register(Banque, BanqueAdmin)
