"""RealEstate app admin.py."""
from django.contrib import admin

from .models import Mandat, RealEstate


class SocieteAdmin(admin.ModelAdmin):
    """RealEstate admin class."""

    pass


class MandatAdmin(admin.ModelAdmin):
    """Mandat admin class."""

    pass


admin.site.register(RealEstate, SocieteAdmin)
admin.site.register(Mandat, MandatAdmin)
