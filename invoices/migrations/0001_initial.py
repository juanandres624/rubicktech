# Generated by Django 4.0.3 on 2022-10-04 16:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        ('products', '0009_product_has_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Invoice_no', models.CharField(blank=True, max_length=200)),
                ('is_final_customer', models.BooleanField(default=False)),
                ('referral_guide', models.CharField(blank=True, max_length=200)),
                ('payment_method', models.CharField(choices=[('Efectivo', 'Efectivo'), ('Dinero Electrónico', 'Dinero Electrónico'), ('Tarjeta de Crédito/Débito', 'Tarjeta de Crédito/Débito'), ('Otros', 'Otros')], max_length=100)),
                ('subtotal_tax', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_0', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_no_sub_taxes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_no_taxes', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_ice', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_tax_percentage', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_tip', models.DecimalField(decimal_places=2, max_digits=10)),
                ('subtotal_gran_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('billing_customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='billing_customer', to='customers.customer')),
                ('shipping_customer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shipping_customer', to='customers.customer')),
            ],
            options={
                'ordering': ['-modified_date'],
            },
        ),
        migrations.CreateModel(
            name='InvoiceDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=0)),
                ('additional_data_1', models.CharField(blank=True, max_length=100)),
                ('additional_data_2', models.CharField(blank=True, max_length=100)),
                ('additional_data_3', models.CharField(blank=True, max_length=100)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoices.invoice')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
