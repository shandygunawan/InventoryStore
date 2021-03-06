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
from utils.models import GlobalConfig

class Command(BaseCommand):
    help = "Seed Database"
    AMOUNT = 100


    def handle(self, *args, **options):
        print('Setting up seed and faker...')
        fake = Faker()
        fake.add_provider(VehicleProvider)
        seed(1)
        seeder = Seed.seeder()

        # Setting Global Config
        print("Setting up Global Config...")
        GlobalConfig(key="autobackup_location", value="/backup/db/").save()

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

        print("Seeding Incomings...")
        for i in range(self.AMOUNT):

            installment_tenor = randint(1, 12)
            installment_paid = randint(0, installment_tenor)

            incoming = Incoming(
                invoice=fake.swift(),
                delivery_note=fake.swift(),
                price_total=0,
                datetime=fake.date_between(start_date='-30d', end_date='today'),
                payment_method=BaseIgog.payment_method_choices[randint(0, len_payment_method-1)][0],
                installment_tenor=installment_tenor,
                installment_paid=installment_paid,
                # installment_duedate use default (null)
                note=fake.paragraph(nb_sentences=5),
                retrieval_type=BaseIgog.retrieval_choices[randint(0, len_retrieval_type-1)][0],
                # retrieval_date uses default (now)
                supplier=Supplier.objects.all()[randint(0, len_suppliers-1)]
            )
            incoming.save()

            for i in range(5):

                count = randint(1, 100)
                num_return = randint(0, count)

                product = Product.objects.all()[randint(1, len_products-1)]
                incoming_product = IncomingProduct(
                    incoming=incoming,
                    product=product,
                    productid=product.id,
                    productname=product.name,
                    count=count,
                    price_per_count=randint(100000, 10000000),
                    num_return=num_return
                )
                incoming_product.save()

        print("Seeding Outgoings...")
        for i in range(self.AMOUNT):

            installment_tenor = randint(1, 12)
            installment_paid = randint(0, installment_tenor)

            outgoing = Outgoing(
                invoice=fake.swift(),
                delivery_note=fake.swift(),
                price_total=0,
                datetime=fake.date_between(start_date='-30d', end_date='today'),
                payment_method=BaseIgog.payment_method_choices[randint(0, len_payment_method-1)][0],
                installment_tenor=installment_tenor,
                installment_paid=installment_paid,
                # installment_duedate use default (null)
                note=fake.paragraph(nb_sentences=5),
                retrieval_type=BaseIgog.retrieval_choices[randint(0, len_retrieval_type-1)][0],
                # retrieval_date uses default (now)
                buyer=Buyer.objects.all()[randint(0, len_buyers-1)]
            )
            outgoing.save()

            for i in range(5):
                count = randint(1, 100)
                num_return = randint(0, count)

                product = Product.objects.all()[randint(1, len_products-1)]
                outgoing_product = OutgoingProduct(
                    outgoing=outgoing,
                    product=product,
                    productid=product.id,
                    productname=product.name,
                    count=count,
                    price_per_count=randint(100000, 10000000),
                    num_return=num_return
                )
                outgoing_product.save()
