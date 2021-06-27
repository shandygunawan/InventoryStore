import random
from django.core.management.base import BaseCommand, CommandError
from random import seed
from random import randint

from faker import Faker
from faker_vehicle import VehicleProvider

from django_seed import Seed

from products.models import Product
from entities.models import Buyer, Supplier
from igog.models import Incoming, IncomingProduct, IncomingDeliveryNote
from igog.models import Outgoing, OutgoingProduct, OutgoingDeliveryNote

class Command(BaseCommand):
    help = "Seed Database"
    AMOUNT = 1000

    def handle(self, *args, **options):
        print('Setting up seed and faker...')
        fake = Faker()
        fake.add_provider(VehicleProvider)
        seed(1)
        seeder = Seed.seeder()

        # Add Supplier
        print("Seeding suppliers...")
        for i in range(self.AMOUNT):
            s = Supplier(
                name=fake.company(),
                phone_number=fake.msisdn(),
                email=fake.company_email(),
                address=fake.address()
            )
            s.save()

        # Add buyer
        print("Seeding buyers...")
        for i in range(self.AMOUNT):
            b = Buyer(
                name=fake.name(),
                phone_number=fake.msisdn(),
                num_ktp=fake.msisdn(),
                num_npwp=fake.msisdn(),
            )
            b.save()

        # Add Product
        print("Seeding products...")
        for i in range(self.AMOUNT):
            p = Product(
                name=fake.vehicle_make_model(),
                stock=randint(0, 100),
                price=randint(100000, 100000000)
            )
            p.save()

        # print("Seeding Incoming...")
        # print("Seeding Outgoing...")
