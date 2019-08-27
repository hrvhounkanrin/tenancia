from django.contrib import admin

from .models import Banque
# Register your models here


class BanqueAdmin(admin.ModelAdmin):
    list_display = ('codebanque', 'libbanque', 'pays')


admin.site.register(Banque, BanqueAdmin)
