from django.contrib import admin
from .models import MngDocumentType, MngCity, MngPersonType, MngProductCategory,MngProductBrand,MngStatus,MngValues,MngFactElect


class MngDocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngPersonTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngCityAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')

class MngProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')
    
class MngProductBrandAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')
    
class MngStatusAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active', 'date_added')
    
class MngValuesAdmin(admin.ModelAdmin):
    list_display = ('description','value', 'is_active', 'date_added')
    
class MngFactElectAdmin(admin.ModelAdmin):
    list_display = ('is_active', 'date_added')


admin.site.register(MngDocumentType, MngDocumentTypeAdmin)
admin.site.register(MngPersonType, MngPersonTypeAdmin)
admin.site.register(MngCity, MngCityAdmin)
admin.site.register(MngProductCategory, MngProductCategoryAdmin)
admin.site.register(MngProductBrand, MngProductBrandAdmin)
admin.site.register(MngStatus, MngStatusAdmin)
admin.site.register(MngValues, MngValuesAdmin)
admin.site.register(MngFactElect, MngFactElectAdmin)