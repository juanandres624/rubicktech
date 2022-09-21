# Generated by Django 4.1 on 2022-09-21 07:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_mngproductbrand'),
        ('providers', '0001_initial'),
        ('products', '0004_remove_product_images_product_boughtprice_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='mngProductBrand_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.mngproductbrand'),
        ),
        migrations.AlterField(
            model_name='product',
            name='mngProductCategory_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.mngproductcategory'),
        ),
        migrations.AlterField(
            model_name='product',
            name='provider_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='providers.provider'),
        ),
    ]
