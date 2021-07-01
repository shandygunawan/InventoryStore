from django.db import models
from django.utils import timezone
from products.models import Product
from entities.models import Supplier, Buyer


#
# BASE CLASSES
#
class BaseIgog(models.Model):

    payment_method_cash = "cash"
    payment_method_transfer = "transfer"
    payment_method_giro = "giro"
    payment_method_choices = [
        (payment_method_cash, "Cash"),
        (payment_method_transfer, "Transfer"),
        (payment_method_giro, "Giro")
    ]

    # payment_status_notstarted = "not_started"
    # payment_status_installment = "installment"
    # payment_status_finished = "finished"
    # payment_status_choices = [
    #     (payment_status_notstarted, "Not Yet Started"),
    #     (payment_status_installment, "Installment"),
    #     (payment_status_finished, "Finished")
    # ]

    retrieval_pickup = "pickup"
    retrieval_delivery = "delivery"
    retrieval_choices = [(retrieval_pickup, "Pickup"), (retrieval_delivery, "Delivery")]

    # Fields
    invoice = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)
    payment_method = models.TextField(choices=payment_method_choices, default=payment_method_cash)
    # payment_status = models.TextField(choices=payment_status_choices, default=payment_status_notstarted)
    installment_tenor = models.PositiveIntegerField(null=True)
    installment_month = models.PositiveIntegerField(null=True)
    installment_duedate = models.DateField(null=True)
    note = models.TextField()

    delivery_note = models.TextField()
    retrieval_type = models.TextField(choices=retrieval_choices, default=retrieval_delivery)
    retrieval_date = models.DateField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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
