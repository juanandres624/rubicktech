from django.db import models
from customers.models import Customer
from products.models import Product

class Invoice(models.Model):

    payment_method_s = (('Efectivo', 'Efectivo'), ('Dinero Electrónico', 'Dinero Electrónico'),
    ('Tarjeta de Crédito/Débito', 'Tarjeta de Crédito/Débito'), ('Otros', 'Otros'),)

    Invoice_no = models.CharField(max_length=200, blank=True)
    billing_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_final_customer = models.BooleanField(default=False)
    referral_guide = models.CharField(max_length=200, blank=True) #Guia de Remision
    payment_method = models.CharField(max_length=20, choices=payment_method_s)
    subtotal_12 = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_0 = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_no_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_discount = models.DecimalField(max_digits=10, decimal_places=2)

    created_date = models.DateTimeField(auto_now_add=True)
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


