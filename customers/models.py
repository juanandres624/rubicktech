from django.db import models
from management.models import MngDocumentType, MngPersonType, MngCity

class Customer(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=True)
    last_name = models.CharField(max_length=100, null=False, blank=True)
    mngPersonType_id = models.ForeignKey(MngPersonType, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    phone_1 = models.CharField(max_length=50, null=False, blank=True)
    phone_2 = models.CharField(max_length=50, null=False, blank=True)
    mngDocumentType_id = models.ForeignKey(MngDocumentType, on_delete=models.CASCADE)
    #document_number = models.CharField(max_length=50, null=False, blank=True)
    document_number = models.IntegerField(unique=True)
    address = models.CharField(max_length=200, null=False, blank=True)
    mngCity_id = models.ForeignKey(MngCity, on_delete=models.CASCADE)
    note = models.CharField(max_length=200, null=False, blank=True)
  
    # required
    is_active = models.BooleanField(default=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.document_number) + ' - ' + self.first_name + ' ' + self.last_name

