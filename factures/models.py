"""Facture app models."""
from django.conf import settings
from django.db import models
from datetime import date
from decimal import Decimal
from jsonfield import JSONField
from proprietaire.models import Proprietaire
from tools import format_currency


class Currency(models.Model):
    """Curency model."""

    code = models.CharField(unique=True, max_length=3)
    pre_symbol = models.CharField(blank=True, max_length=1)
    post_symbol = models.CharField(blank=True, max_length=1)
    created_at = models.ForeignKey(auto_now_add=True)
    modified_at = models.ForeignKey(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="currency_created_user"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="currency_updated_user"
    )

    def __str__(self):
        """Currency to string."""
        return self.code


class InvoiceManager(models.Manager):
    """Invoicemanager."""

    def get_invoiced(self):
        """Get invoice."""
        return self.filter(invoiced=True, draft=False)

    def get_due(self):
        """Get invoice due."""
        return self.filter(invoice_date__lte=date.today(),
                           invoiced=False, draft=False)


class Item(models.Model):
    """Invoice item."""

    ACTIVE = 1
    INACTIVE = 0
    DISABLED = -1
    ITEM_STATE = (
        (ACTIVE, "Item Active"),
        (INACTIVE, "Item Inactive"),
        (DISABLED, "Item Disabled"),
    )
    name = models.CharField(max_length=100, default="")
    activation_status = models.SmallIntegerField(
        choices=ITEM_STATE, blank=True, null=True
    )
    measurement = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="user"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="user"
    )

    def __str__(self):
        """Item to string."""
        return self.name

    class Meta:
        """Item meta class."""

        ordering = ["-id"]


class Invoice(models.Model):
    """Invoice model."""

    client = JSONField(default=dict())
    proprietaire = models.ForeignKey(Proprietaire, on_delete=models.CASCADE)
    currency = models.ForeignKey(
        Currency, blank=True, null=True, on_delete=models.CASCADE
    )
    invoice_id = models.CharField(
        unique=True, max_length=6, null=True, blank=True, editable=False
    )
    invoice_date = models.DateField(default=date.today)
    invoiced = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    appartement = JSONField(default=dict())
    created_at = models.ForeignKey(auto_now_add=True)
    modified_at = models.ForeignKey(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="invoice_created_user"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="invoice_updated_user"
    )

    def __str__(self):
        """Convert invoice to string."""
        return u"%s (%s)" % (self.invoice_id, self.total_amount())

    class Meta:
        """Invoice model meta class."""

        ordering = ("-invoice_date", "id")

    def total_amount(self):
        """Invoice total amount."""
        return format_currency(self.total(), self.currency)

    def total(self):
        """Get invoice total."""
        total = Decimal("0.00")
        for item in self.items.all():
            total = total + item.total()
        return total

    def file_name(self):
        """Get invoice fileName."""
        return u"Invoice %s.pdf" % self.invoice_id


class InvoiceItem(models.Model):
    """Invoice item."""

    invoice = models.ForeignKey(
        Invoice, related_name="items", unique=False, on_delete=models.CASCADE
    )
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)
    created_at = models.ForeignKey(auto_now_add=True)
    modified_at = models.ForeignKey(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="invoiceitem_created_user"
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL,
        editable=False, related_name="invoiceitem_created_user"
    )

    def total(self):
        """Get invoice total."""
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal("0.01"))

    def __str__(self):
        """Convert invoice to string."""
        return self.description
