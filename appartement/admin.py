from django.contrib import admin

from .models import Appartement


class AppartmAdmin(admin.ModelAdmin):
    list_display = ['id', 'intitule', 'level', 'immeuble', 'structure', 'statut']

admin.register(Appartement, AppartmAdmin)
