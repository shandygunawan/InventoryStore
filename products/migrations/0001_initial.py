# Generated by Django 3.2 on 2021-06-13 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('stock', models.PositiveBigIntegerField(default=0)),
                ('price', models.PositiveBigIntegerField(default=0)),
                ('image', models.ImageField(default='placeholders/products.jpg', upload_to='products_images')),
            ],
        ),
    ]
