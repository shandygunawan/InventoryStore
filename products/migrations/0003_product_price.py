# Generated by Django 3.2 on 2021-05-08 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_product_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.PositiveBigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
