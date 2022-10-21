from django.db import models
from customers.models import Customer
from products.models import Product
from accounts.models import Account
from django.utils import timezone

class Invoice(models.Model):

    payment_method_s = (('Efectivo', 'Efectivo'), ('Dinero Electrónico', 'Dinero Electrónico'),
    ('Tarjeta de Crédito/Débito', 'Tarjeta de Crédito/Débito'), ('Otros', 'Otros'),)

    Invoice_no = models.CharField(max_length=200, blank=True)
    billing_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name= 'billing_customer')
    shipping_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name = 'shipping_customer')
    is_final_customer = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    referral_guide = models.CharField(max_length=200, blank=True) #Guia de Remision
    payment_method = models.CharField(max_length=100, choices=payment_method_s)
    subtotal_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0) #Subtotal 12%
    subtotal_0 = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Subtotal 0%
    subtotal_no_sub_taxes = models.DecimalField(max_digits=10, decimal_places=2 , default=0) # Subtotal No Sujeto De IVA
    subtotal_no_taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Subtotal Sin Impuestos
    subtotal_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuento
    subtotal_ice = models.DecimalField(max_digits=10, decimal_places=2, default=0) # ICE
    subtotal_tax_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0) # IVA 12%
    subtotal_tip = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Propina
    subtotal_gran_total = models.DecimalField(max_digits=10, decimal_places=2, default=0) # Valor TOTAL

    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    paid_date = models.DateTimeField(blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.Invoice_no

    class Meta:
        ordering = ['-modified_date']


class InvoiceDetail(models.Model):
    
    invoice_id = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    additional_data_1 = models.CharField(max_length=100, blank=True)
    additional_data_2 = models.CharField(max_length=100, blank=True)
    additional_data_3 = models.CharField(max_length=100, blank=True)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)


