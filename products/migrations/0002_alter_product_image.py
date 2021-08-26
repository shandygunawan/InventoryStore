# Generated by Django 3.2 on 2021-08-26 11:24

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='placeholders/products.jpg', storage=products.models.OverwriteStorage(location='C:\\Users\\Shandy\\Projects\\PycharmProjects\\InventoryStore\\media/product_images'), upload_to='products_images'),
        ),
    ]
