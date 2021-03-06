# Generated by Django 3.2 on 2021-04-09 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0001_initial'),
        ('retailer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='details',
            name='product_catagory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='product.catagory'),
        ),
        migrations.AddField(
            model_name='details',
            name='retailer_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='retailer.details'),
        ),
    ]
