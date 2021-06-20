from django.db import models
from django.utils import timezone
from products.models import Product
from entities.models import Supplier, Buyer
from datetime import date

#
# BASE CLASSES
#

class BaseIgog(models.Model):
    # Local Variables
    payment_method_cash = "cash"
    payment_method_transfer = "transfer"
    payment_method_giro = "giro"
    payment_method_choices = [
        (payment_method_cash, "Cash"),
        (payment_method_transfer, "Transfer"),
        (payment_method_giro, "Giro")
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
    payment_method = models.TextField(choices=payment_method_choices, default=payment_method_cash)
    payment_status = models.TextField(choices=payment_status_choices, default=payment_status_notstarted)
    due_date = models.DateField(null=True)


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
    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.datetime.strftime('%Y-%m-%d %H:%M')

class IncomingProduct(models.Model):
    incoming = models.ForeignKey(Incoming, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.PositiveBigIntegerField()
    price_per_count = models.PositiveBigIntegerField()

class IncomingDeliveryNote(BaseDeliveryNote):
    incoming = models.OneToOneField(Incoming, on_delete=models.CASCADE, primary_key=True)


#
# OUTGOING CLASSES
#
class Outgoing(BaseIgog):
    # Many to Many
    products = models.ManyToManyField(
        Product,
        through="OutgoingProduct",
        through_fields=('outgoing', 'product')
    )
    buyer = models.ForeignKey(Buyer, null=True, on_delete=models.SET_NULL)


class OutgoingProduct(models.Model):
    outgoing = models.ForeignKey(Outgoing, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.PositiveBigIntegerField()
    price_per_count = models.PositiveBigIntegerField()

class OutgoingDeliveryNote(BaseDeliveryNote):
    outgoing = models.OneToOneField(Outgoing, on_delete=models.CASCADE, primary_key=True)
