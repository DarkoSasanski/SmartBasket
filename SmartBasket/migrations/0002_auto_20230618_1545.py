# Generated by Django 3.2.18 on 2023-06-18 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SmartBasket', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryorder',
            name='delivered',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pickuporder',
            name='picked_up',
            field=models.BooleanField(default=False),
        ),
    ]
