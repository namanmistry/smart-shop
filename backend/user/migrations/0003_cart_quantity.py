# Generated by Django 3.2 on 2021-04-10 05:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_orders_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='quantity',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
