# Generated by Django 3.2.6 on 2021-10-15 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
        ('sales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='portfolio',
            field=models.ManyToManyField(blank=True, null=True, to='products.Product'),
        ),
    ]
