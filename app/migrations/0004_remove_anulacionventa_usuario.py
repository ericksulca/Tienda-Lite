# Generated by Django 2.1 on 2018-08-31 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20180831_1519'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anulacionventa',
            name='usuario',
        ),
    ]
