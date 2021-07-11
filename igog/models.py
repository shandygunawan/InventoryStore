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

    retrieval_pickup = "pickup"
    retrieval_delivery = "delivery"
    retrieval_choices = [(retrieval_pickup, "Pickup"), (retrieval_delivery, "Delivery")]

    # Fields
    invoice = models.TextField()
    datetime = models.DateTimeField(default=timezone.now)
    price_total = models.PositiveBigIntegerField(default=0)
    payment_method = models.TextField(choices=payment_method_choices, default=payment_method_cash)
    installment_tenor = models.PositiveIntegerField(default=1)
    installment_paid = models.PositiveIntegerField(default=0)
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
    incoming = models.ForeignKey(Incoming, null=True, on_delete=models.CASCADE)
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
    outgoing = models.ForeignKey(Outgoing, null=True, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    count = models.PositiveBigIntegerField()
    price_per_count = models.PositiveBigIntegerField()
