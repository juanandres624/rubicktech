from asyncio.windows_events import NULL
from django.db import models
from providers.models import Provider
from management.models import MngProductCategory,MngProductBrand


class Product(models.Model):
    product_code = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=200, blank=True)
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    boughtPrice = models.DecimalField(max_digits=10, decimal_places=2)
    #images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField(default=0)
    is_discount = models.BooleanField(default=False)
    discountPorcentage = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    mngProductCategory_id = models.ForeignKey(MngProductCategory, on_delete=models.CASCADE)
    mngProductBrand_id = models.ForeignKey(MngProductBrand, on_delete=models.CASCADE)
    provider_id = models.ForeignKey(Provider, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    # def get_url(self):
    #     return reverse('product_detail', args=[self.category.slug, self.slug])

    class Meta:
        ordering = ['-modified_date']

class Image(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products')
    default = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

variation_category_choice = (
    ('color', 'color'),
    ('size', 'size'),
)


class VariationManager(models.Manager):
    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)

    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class Variation(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value