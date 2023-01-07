# Generated by Django 4.1 on 2023-01-07 03:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('invoices', '0018_alter_invoice_payment_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_m_inv', to=settings.AUTH_USER_MODEL),
        ),
    ]
