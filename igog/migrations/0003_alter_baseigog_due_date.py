# Generated by Django 3.2 on 2021-06-23 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('igog', '0002_remove_baseigog_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baseigog',
            name='due_date',
            field=models.DateField(null=True),
        ),
    ]
