# Generated by Django 2.0.6 on 2018-07-24 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
        ('modulos', '0003_auto_20180723_2210'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permisos',
            new_name='Permiso',
        ),
    ]
