# Generated by Django 4.2.4 on 2023-10-29 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_remove_product_image_remove_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='returned',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
