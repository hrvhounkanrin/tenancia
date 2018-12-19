from django.contrib import admin

from . models import Appartement
# Register your models here.
class AppartmAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('intitule', 'level', 'immeuble', 'structure', 'statut')
    # search_fields = ('id','nom')

admin.register(AppartmAdmin, Appartement)