"""Facture admin."""
from django.contrib import admin
from factures.models import \
    (Currency, Item, Invoice, InvoiceItem)


class InvoiceAdmin(admin.ModelAdmin):
    """Invoice admin class."""

    list_display = "__all__"
    search_fields = ("id",)


class CurrencyAdmin(admin.ModelAdmin):
    """Currency admin class."""

    list_display = "__all__"
    search_fields = ("id",)


class ItemAdmin(admin.ModelAdmin):
    """Item admin class."""

    list_display = "__all__"


class InvoiceItemAdmin(admin.ModelAdmin):
    """Invoice item admin class."""

    list_display = "__all__"
    search_fields = ("id",)


admin.register(Invoice, InvoiceAdmin)
admin.register(Currency, CurrencyAdmin)
admin.register(InvoiceItem, InvoiceItemAdmin)
admin.register(Item, ItemAdmin)
