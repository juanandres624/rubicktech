from django.contrib import admin
from .models import Invoice


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('Invoice_no', 'billing_customer_id', 'user', 'mngStatus_id', 'created_date')


admin.site.register(Invoice, InvoiceAdmin)
