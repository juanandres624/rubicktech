# Generated by Django 4.1 on 2022-11-15 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0011_mngfactelect_codimp'),
    ]

    operations = [
        migrations.AddField(
            model_name='mngfactelect',
            name='tarifIva',
            field=models.CharField(choices=[('0', '0% '), ('2', '12%'), ('3', '14%'), ('6', 'No Objeto de Impuesto'), ('7', 'Exento de IVA'), ('8', 'IVA diferenciado')], default=2, max_length=1),
            preserve_default=False,
        ),
    ]
