import random

from django.core.management.base import BaseCommand, CommandError

from django_seed import Seed

from products.models import Product
from entities.models import Buyer, Supplier
from igog.models import Incoming, IncomingProduct, IncomingSupplier, IncomingDeliveryNote
from igog.models import Outgoing, OutgoingProduct, OutgoingBuyer, OutgoingDeliveryNote

class Command(BaseCommand):
    help = "Seed Database"

    def handle(self, *args, **options):
        seeder = Seed.seeder()

        seeder.add_entity(Supplier, 20)
        seeder.add_entity(Buyer, 20)
        seeder.add_entity(Product, 10, {
            'stock': lambda x: random.randint(0, 100),
            'price': lambda x: random.randint(0, 100000),
        })

        seeder.add_entity(Incoming, 25, {
            'total_price': lambda x: random.randint(0, 100000000)
        })
        seeder.add_entity(IncomingProduct, 50, {
            'count': lambda x: random.randint(0, 1000),
            'price_per_count': lambda x: random.randint(0, 100000000)
        })
        seeder.add_entity(IncomingSupplier, 20)
        # seeder.add_entity(IncomingDeliveryNote, 25)

        seeder.add_entity(Outgoing, 25, {
            'total_price': lambda x: random.randint(0, 100000000)
        })
        seeder.add_entity(OutgoingProduct, 50, {
            'count': lambda x: random.randint(0, 1000),
            'price_per_count': lambda x: random.randint(0, 100000000)
        })
        seeder.add_entity(OutgoingBuyer, 20)
        # seeder.add_entity(OutgoingDeliveryNote, 25)

        seeder.execute()