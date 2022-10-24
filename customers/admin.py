from django.contrib import admin
from .models import Customer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('document_number', 'first_name', 'last_name', 'email', 'date_added')


admin.site.register(Customer, CustomerAdmin)
