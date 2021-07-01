import random
import string
from django.core.management.base import BaseCommand, CommandError
from random import seed
from random import randint

from faker import Faker
from faker_vehicle import VehicleProvider

from django_seed import Seed

from products.models import Product
from entities.models import Buyer, Supplier
from igog.models import (
    BaseIgog,
    Incoming,
    IncomingProduct,
    Outgoing, OutgoingProduct
)

class Command(BaseCommand):
    help = "Seed Database"
    AMOUNT = 100


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
                name=fake.vehicle_year_make_model_cat(),
                stock=randint(0, 100),
                price=randint(100000, 100000000)
            )
            p.save()

        len_payment_method = len(BaseIgog.payment_method_choices)
        len_retrieval_type = len(BaseIgog.retrieval_choices)
        len_products = Product.objects.all().count()
        len_suppliers = Supplier.objects.all().count()
        len_buyers = Buyer.objects.all().count()

        print("Seeding Incoming...")
        for i in range(self.AMOUNT):

            installment_tenor = randint(1, 12)
            installment_month = abs(installment_tenor - randint(0, 12))

            incoming = Incoming(
                invoice=fake.swift(),
                delivery_note=fake.swift(),
                datetime=fake.date_between(start_date='-30d', end_date='today'),
                payment_method=BaseIgog.payment_method_choices[randint(0, len_payment_method-1)][0],
                installment_tenor=installment_tenor,
                installment_month=installment_month,
                # installment_duedate use default (null)
                note=fake.paragraph(nb_sentences=5),
                retrieval_type=BaseIgog.retrieval_choices[randint(0, len_retrieval_type-1)][0],
                # retrieval_date uses default (now)
                supplier=Supplier.objects.all()[randint(0, len_suppliers-1)]
            )
            incoming.save()

            for i in range(5):
                incoming_product = IncomingProduct(
                    incoming=incoming,
                    product=Product.objects.all()[randint(1, len_products-1)],
                    count=randint(1, 100),
                    price_per_count=randint(100000, 10000000)
                )
                incoming_product.save()

        print("Seeding Outgoing...")
        for i in range(self.AMOUNT):

            installment_tenor = randint(1, 12)
            installment_month = abs(installment_tenor - randint(0, 12))

            outgoing = Outgoing(
                invoice=fake.swift(),
                delivery_note=fake.swift(),
                datetime=fake.date_between(start_date='-30d', end_date='today'),
                payment_method=BaseIgog.payment_method_choices[randint(0, len_payment_method-1)][0],
                installment_tenor=installment_tenor,
                installment_month=installment_month,
                # installment_duedate use default (null)
                note=fake.paragraph(nb_sentences=5),
                retrieval_type=BaseIgog.retrieval_choices[randint(0, len_retrieval_type-1)][0],
                # retrieval_date uses default (now)
                buyer=Buyer.objects.all()[randint(0, len_buyers-1)]
            )
            outgoing.save()

            for i in range(5):
                outgoing_product = OutgoingProduct(
                    outgoing=outgoing,
                    product=Product.objects.all()[randint(1, len_products-1)],
                    count=randint(1, 100),
                    price_per_count=randint(100000, 10000000)
                )
                outgoing_product.save()
