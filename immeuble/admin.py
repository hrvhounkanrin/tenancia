from django.contrib import admin

from .models import Immeuble
# Register your models here.


class ImmeubleAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['id', 'intitule', 'description', 'adresse',
                    'proprietaire', 'jour_emission_facture',
                    'jour_valeur_facture', 'ville', 'quartier',
                    'pays', 'longitude', 'latitude', 'ref_immeuble']

    list_display_links = ['id',]


admin.site.register(Immeuble, ImmeubleAdmin)
