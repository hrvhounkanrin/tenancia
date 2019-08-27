from django.contrib import admin

# Register your models here

from .models import Banque


class BanqueAdmin(admin.ModelAdmin):
    list_display = ('codebanque', 'libbanque', 'pays')


admin.site.register(Banque, BanqueAdmin)
