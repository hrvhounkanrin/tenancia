from django.contrib import admin
from .models import *


class ProprietaireAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ['id', 'mode_paiement',
                    'numcompte',
                    'user',
                    'banque',
                    'pays_residence', ]

    list_display_links = ['id',]


admin.site.register(Proprietaire, ProprietaireAdmin)
