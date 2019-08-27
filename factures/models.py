from datetime import date
from decimal import Decimal
from jsonfield import JSONField
from django_extensions.db.models import TimeStampedModel
from client.models import *
from proprietaire.models import *
from tools import format_currency
from appartement.models import *


class Currency(models.Model):
    code = models.CharField(unique=True, max_length=3)
    pre_symbol = models.CharField(blank=True, max_length=1)
    post_symbol = models.CharField(blank=True, max_length=1)

    def __str__(self):
        return self.code


class InvoiceManager(models.Manager):
    def get_invoiced(self):
        return self.filter(invoiced=True, draft=False)

    def get_due(self):
        return self.filter(invoice_date__lte=date.today(),
                           invoiced=False,
                           draft=False)


class Item(models.Model):
    ACTIVE = 1
    INACTIVE = 0
    DISABLED = -1
    ITEM_STATE = (
        (ACTIVE, 'Item Active'),
        (INACTIVE, 'Item Inactive'),
        (DISABLED, 'Item Disabled'),
        )
    name = models.CharField(max_length=100, default='')
    activation_status = models.SmallIntegerField(choices=ITEM_STATE, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    measurement = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Invoice(TimeStampedModel):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE)
    proprietaire = models.ForeignKey(Proprietaire,
                                     on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, blank=True, null=True,
                                 on_delete=models.CASCADE)
    invoice_id = models.CharField(unique=True,
                                  max_length=6, null=True,
                                  blank=True, editable=False)
    invoice_date = models.DateField(default=date.today)
    invoiced = models.BooleanField(default=False)
    draft = models.BooleanField(default=False)
    paid_date = models.DateField(blank=True, null=True)
    appartement = JSONField(default=dict())

    objects = InvoiceManager()

    def __str__(self):
        return u'%s (%s)' % (self.invoice_id, self.total_amount())

    class Meta:
        ordering = ('-invoice_date', 'id')

    def total_amount(self):
        return format_currency(self.total(), self.currency)

    def total(self):
        total = Decimal('0.00')
        for item in self.items.all():
            total = total + item.total()
        return total

    def file_name(self):
        return u'Invoice %s.pdf' % self.invoice_id

    # def send_invoice(self):
    #     pdf = StringIO()
    #     draw_pdf(pdf, self)
    #     pdf.seek(0)
    #
    #     attachment = MIMEApplication(pdf.read())
    #     attachment.add_header("Content-Disposition", "attachment",
    #                           filename=self.file_name())
    #     pdf.close()
    #
    #     subject = app_settings.INV_EMAIL_SUBJECT % {"invoice_id": self.invoice_id}
    #     email_kwargs = {
    #         "invoice": self,
    #         "SITE_NAME": settings.SITE_NAME,
    #         "INV_CURRENCY": app_settings.INV_CURRENCY,
    #         "INV_CURRENCY_SYMBOL": app_settings.INV_CURRENCY_SYMBOL,
    #         "SUPPORT_EMAIL": settings.MANAGERS[0][1],
    #         }
    #     try:
    #         template = get_template("invoice/invoice_email.html")
    #         body = template.render(Context(email_kwargs))
    #     except TemplateDoesNotExist:
    #         body = render_to_string("invoice/invoice_email.txt", email_kwargs)
    #     email = EmailMultiAlternatives(subject=subject, body=strip_tags(body), to=[self.user.email])
    #     email.attach_alternative(body, "text/html")
    #     email.attach(attachment)
    #     email.send()
    #
    #     self.invoiced = True
    #     self.save()


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', unique=False,
                                on_delete=models.CASCADE)
    description = models.CharField(max_length=100)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, default=1)

    def total(self):
        total = Decimal(str(self.unit_price * self.quantity))
        return total.quantize(Decimal('0.01'))

    def __str__(self):
        return self.description
