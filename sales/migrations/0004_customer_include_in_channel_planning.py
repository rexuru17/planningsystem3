# Generated by Django 3.2.6 on 2021-10-16 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_auto_20211015_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='include_in_channel_planning',
            field=models.BooleanField(default=False),
        ),
    ]
