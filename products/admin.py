from django.contrib import admin
from .models import Product, Variation,Image


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'description', 'price', 'stock',   'is_available', 'modified_date')
    prepopulated_fields = {'slug': ('product_name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product_id', 'variation_category', 'variation_value')

class ImageAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name','image')
    list_filter = ('product_id', 'name', 'image')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(Image, ImageAdmin)