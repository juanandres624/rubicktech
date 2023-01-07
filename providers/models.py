from django.db import models
from management.models import MngDocumentType, MngCity
from accounts.models import Account

class Provider(models.Model):
    provider_code = models.CharField(max_length=100, null=False, blank=True)
    business_reason = models.CharField(max_length=200, null=False, blank=True) #razon comercial
    social_reason = models.CharField(max_length=100, null=False, blank=True) #razon social
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    phone_1 = models.CharField(max_length=50, null=False, blank=True)
    phone_2 = models.CharField(max_length=50, null=False, blank=True)
    mngDocumentType_id = models.ForeignKey(MngDocumentType, on_delete=models.CASCADE)
    document_number = models.CharField(max_length=50, null=False, blank=True)
    address_1 = models.CharField(max_length=200, null=False, blank=True)
    address_2 = models.CharField(max_length=200, null=False, blank=True)
    city = models.ForeignKey(MngCity, on_delete=models.CASCADE)
    web_site = models.CharField(max_length=250, null=False, blank=True)
    note = models.CharField(max_length=200, null=False, blank=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(Account, on_delete=models.CASCADE, null=True,related_name= 'created_by_m_prov')

    # required
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.provider_code + '-' + self.business_reason