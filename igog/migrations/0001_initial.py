# Generated by Django 3.2 on 2021-07-13 10:32

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        ('entities', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseIgog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice', models.TextField()),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('price_total', models.PositiveBigIntegerField(default=0)),
                ('payment_method', models.TextField(choices=[('cash', 'Cash'), ('transfer', 'Transfer'), ('giro', 'Giro')], default='cash')),
                ('installment_tenor', models.PositiveIntegerField(default=1)),
                ('installment_paid', models.PositiveIntegerField(default=0)),
                ('installment_duedate', models.DateField(null=True)),
                ('note', models.TextField()),
                ('delivery_note', models.TextField()),
                ('retrieval_type', models.TextField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], default='delivery')),
                ('retrieval_date', models.DateField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('baseigog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='igog.baseigog')),
            ],
            bases=('igog.baseigog',),
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('baseigog_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='igog.baseigog')),
                ('buyer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.buyer')),
            ],
            bases=('igog.baseigog',),
        ),
        migrations.CreateModel(
            name='OutgoingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.PositiveBigIntegerField()),
                ('productname', models.TextField()),
                ('count', models.PositiveBigIntegerField()),
                ('price_per_count', models.PositiveBigIntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('outgoing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='igog.outgoing')),
            ],
        ),
        migrations.AddField(
            model_name='outgoing',
            name='products',
            field=models.ManyToManyField(through='igog.OutgoingProduct', to='products.Product'),
        ),
        migrations.CreateModel(
            name='IncomingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productid', models.PositiveBigIntegerField()),
                ('productname', models.TextField()),
                ('count', models.PositiveBigIntegerField()),
                ('price_per_count', models.PositiveBigIntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('incoming', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='igog.incoming')),
            ],
        ),
        migrations.AddField(
            model_name='incoming',
            name='products',
            field=models.ManyToManyField(through='igog.IncomingProduct', to='products.Product'),
        ),
        migrations.AddField(
            model_name='incoming',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.supplier'),
        ),
    ]
