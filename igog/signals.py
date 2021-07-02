from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from igog.models import (
    IncomingProduct,
    OutgoingProduct
)


@receiver(post_save, sender=IncomingProduct)
def incoming_total_price_increase(sender, instance, created, **kwargs):
    if created:
        instance.incoming.price_total += (instance.count * instance.price_per_count)
        instance.incoming.save()

@receiver(post_delete, sender=IncomingProduct)
def incoming_total_price_decrease(sender, instance, **kwargs):
    instance.incoming.price_total -= (instance.count * instance.price_per_count)
    instance.incoming.save()

@receiver(post_save, sender=OutgoingProduct)
def outgoing_total_price_increase(sender, instance, created, **kwargs):
    if created:
        instance.outgoing.price_total += (instance.count * instance.price_per_count)
        instance.outgoing.save()

@receiver(post_delete, sender=OutgoingProduct)
def outgoing_total_price_decrease(sender, instance, **kwargs):
    instance.outgoing.price_total -= (instance.count * instance.price_per_count)
    instance.outgoing.save()