from email.policy import default
from django.db import models
from customers.models import Customer
from products.models import Product
from accounts.models import Account
from management.models import MngStatus
from django.utils import timezone
from django.db.models import Max
from management.models import MngPaymentType

def invoice_number():
    invid = Invoice.objects.aggregate(max_inv=Max('Invoice_no'))['max_inv']
    if invid is not None:
        return invid + 1
    return 0

class Invoice(models.Model):

    Invoice_no = models.IntegerField(default=invoice_number, unique=True)
    Invoice_no_final = models.CharField(max_length=200, blank=True)
    billing_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name= 'billing_customer',blank=True,null=True)
    #shipping_customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name = 'shipping_customer')
    is_final_customer = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    referral_guide = models.CharField(max_length=200, blank=True) #Guia de Remision
    payment_method = models.ForeignKey(MngPaymentType, on_delete=models.CASCADE)
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
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,related_name= 'created_by_m_inv')
    mngStatus_id = models.ForeignKey(MngStatus, on_delete=models.CASCADE, default=1)


    paid_date = models.DateTimeField(blank=True,null=True,default=None)
    created_date = models.DateTimeField(default=timezone.now)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Invoice_no)

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

