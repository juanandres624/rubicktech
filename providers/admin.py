from django.contrib import admin
from .models import Provider


class ProviderAdmin(admin.ModelAdmin):
    list_display = ('provider_code', 'business_reason', 'email', 'is_active', 'date_added')


admin.site.register(Provider, ProviderAdmin)