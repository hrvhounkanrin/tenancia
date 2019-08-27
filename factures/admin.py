from django.contrib import admin

from factures.models import *


# Register your models here.

class InvoiceAdmin(admin.ModelAdmin):
    list_display = '__all__'
    search_fields = ('id',)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = '__all__'
    search_fields = ('id',)


class ItemAdmin(admin.ModelAdmin):
    list_display = '__all__'


class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = '__all__'
    search_fields = ('id',)


admin.register(Invoice, InvoiceAdmin)
admin.register(Currency, CurrencyAdmin)
admin.register(InvoiceItem, InvoiceItemAdmin)
admin.register(Item, ItemAdmin)
