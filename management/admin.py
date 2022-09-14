from django.contrib import admin
from .models import MngDocumentType, MngCity, MngPersonType, MngProductCategory


class MngDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngPersonTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngCityAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')


admin.site.register(MngDocumentType, MngDocumentTypeAdmin)
admin.site.register(MngPersonType, MngPersonTypeAdmin)
admin.site.register(MngCity, MngCityAdmin)
admin.site.register(MngProductCategory, MngProductCategoryAdmin)