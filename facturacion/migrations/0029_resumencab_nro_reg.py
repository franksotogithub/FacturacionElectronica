# Generated by Django 2.0.6 on 2018-09-09 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0028_auto_20180909_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumencab',
            name='nro_reg',
            field=models.IntegerField(blank=True, db_column='NRO_REG', null=True),
        ),
    ]