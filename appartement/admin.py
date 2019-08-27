from django.contrib import admin

from .models import Appartement


# Register your models here.
class AppartmAdmin(admin.ModelAdmin):
    list_display = ['id', 'intitule', 'level', 'immeuble', 'structure', 'statut']
    # search_fields = ('id','nom')


admin.register(Appartement, AppartmAdmin)
