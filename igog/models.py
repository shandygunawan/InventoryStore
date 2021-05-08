from django.db import models
from django.utils import timezone
from products.models import Product

#
# BASE CLASSES
#

class BaseIgog(models.Model):
    # Local Variables
    payment_type_cash = "cash"
    payment_type_transfer = "transfer"
    payment_type_giro = "giro"
    payment_type_choices = [
        (payment_type_cash, "Cash"),
        (payment_type_transfer, "Transfer"),
        (payment_type_giro, "Giro")
    ]

    payment_status_notstarted = "not_started"
    payment_status_installment = "installment"
    payment_status_finished = "finished"
    payment_status_choices = [
        (payment_status_notstarted, "Not Yet Started"),
        (payment_status_installment, "Installment"),
        (payment_status_finished, "Finished")
    ]

    # Fields
    datetime = models.DateTimeField(default=timezone.now)
    total_price = models.PositiveBigIntegerField()
    payment_type = models.TextField(choices=payment_type_choices, default=payment_type_cash)
    payment_status = models.TextField(choices=payment_status_choices, default=payment_status_notstarted)
    due_date = models.DateField(default=timezone.now, null=True)


class BaseDeliveryNote(models.Model):
    type_pickup = "pickup"
    type_delivery = "delivery"
    type_choices = [(type_pickup, "Pickup"), (type_delivery, "Delivery")]

    # Fields
    date = models.DateField(default=timezone.now)
    retrieval_type = models.TextField(choices=type_choices, default=type_pickup)


#
# INCOMING CLASSES
#
class Incoming(BaseIgog):
    # Many to Many
    products = models.ManyToManyField(
        Product,
        through="IncomingProduct",
        through_fields=('incoming', 'product')
    )


class IncomingProduct(models.Model):
    incoming = models.ForeignKey(Incoming, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.PositiveBigIntegerField()
    price_per_count = models.PositiveBigIntegerField()


class IncomingDeliveryNote(BaseDeliveryNote):
    incoming_id = models.OneToOneField(Incoming, on_delete=models.CASCADE, primary_key=True)

#
# OUTGOING CLASSES
#