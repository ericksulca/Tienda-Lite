# Generated by Django 2.1 on 2018-09-17 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_apploteproductos'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoteProductos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'app_lote_productos',
                'managed': False,
            },
        ),
    ]
