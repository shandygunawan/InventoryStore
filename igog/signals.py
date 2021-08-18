from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete

from igog.models import (
    IncomingProduct,
    OutgoingProduct
)
from products.models import Product


#
# Total Price increase/decrease
#
@receiver(post_save, sender=IncomingProduct)
def incoming_total_price_increase(sender, instance, created, **kwargs):
    if created:
        print(instance.count)
        print(instance.price_per_count)
        instance.incoming.price_total += ( int(instance.count) * int(instance.price_per_count) )
        instance.incoming.save()

@receiver(pre_delete, sender=IncomingProduct)
def incoming_total_price_decrease(sender, instance, **kwargs):
    instance.incoming.price_total -= ( int(instance.count) * int(instance.price_per_count) )
    instance.incoming.save()

@receiver(post_save, sender=OutgoingProduct)
def outgoing_total_price_increase(sender, instance, created, **kwargs):
    if created:
        instance.outgoing.price_total += ( int(instance.count) * int(instance.price_per_count) )
        instance.outgoing.save()

@receiver(pre_delete, sender=OutgoingProduct)
def outgoing_total_price_decrease(sender, instance, **kwargs):
    instance.outgoing.price_total -= ( int(instance.count) * int(instance.price_per_count) )
    instance.outgoing.save()


#
# Stock Increase/Decrease
#
@receiver(post_save, sender=IncomingProduct)
def incoming_stock_increase(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock += int(instance.count)
        product.save()

@receiver(post_save, sender=OutgoingProduct)
def outgoing_stock_decrease(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        if product.stock - int(instance.count) >= 0:
            product.stock -= int(instance.count)
            product.save()