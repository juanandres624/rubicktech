# Generated by Django 4.1 on 2022-09-01 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('phone_1', models.CharField(blank=True, max_length=50)),
                ('phone_2', models.CharField(blank=True, max_length=50)),
                ('document_number', models.CharField(blank=True, max_length=50)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('note', models.CharField(blank=True, max_length=200)),
                ('is_active', models.BooleanField(default=True)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('mngCity_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.mngcity')),
                ('mngDocumentType_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.mngdocumenttype')),
                ('mngPersonType_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.mngpersontype')),
            ],
        ),
    ]
