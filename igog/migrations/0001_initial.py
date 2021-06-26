# Generated by Django 3.2 on 2021-06-26 14:19

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
            name='BaseDeliveryNote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('retrieval_type', models.TextField(choices=[('pickup', 'Pickup'), ('delivery', 'Delivery')], default='pickup')),
            ],
        ),
        migrations.CreateModel(
            name='BaseIgog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_method', models.TextField(choices=[('cash', 'Cash'), ('transfer', 'Transfer'), ('giro', 'Giro')], default='cash')),
                ('payment_status', models.TextField(choices=[('not_started', 'Not Yet Started'), ('installment', 'Installment'), ('finished', 'Finished')], default='not_started')),
                ('due_date', models.DateField(null=True)),
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
            name='IncomingDeliveryNote',
            fields=[
                ('basedeliverynote_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='igog.basedeliverynote')),
                ('incoming', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='igog.incoming')),
            ],
            bases=('igog.basedeliverynote',),
        ),
        migrations.CreateModel(
            name='OutgoingDeliveryNote',
            fields=[
                ('basedeliverynote_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='igog.basedeliverynote')),
                ('outgoing', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='igog.outgoing')),
            ],
            bases=('igog.basedeliverynote',),
        ),
        migrations.CreateModel(
            name='OutgoingProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveBigIntegerField()),
                ('price_per_count', models.PositiveBigIntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('outgoing', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='igog.outgoing')),
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
                ('count', models.PositiveBigIntegerField()),
                ('price_per_count', models.PositiveBigIntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.product')),
                ('incoming', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='igog.incoming')),
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
