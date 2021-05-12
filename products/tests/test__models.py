from django.test import TestCase
from django.db.utils import IntegrityError
from products.models import Product
from field_history.models import FieldHistory

class ProductTestCase(TestCase):
    # Test Create
    def test_product_create_normal(self):
        product = Product.objects.create(name="test_product_create_normal", stock=100, price=100000)
        product.save()
        product_saved = Product.objects.get(name="test_product_create_normal")
        self.assertEqual(product.name, product_saved.name)

    def test_product_create_null(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name=None, stock=100, price=100000)

    def test_product_create_stock_below_zero(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="test_product_create_stock_below_zero", stock=-1, price=100000)

    def test_product_create_price_below_zero(self):
        with self.assertRaises(IntegrityError):
            Product.objects.create(name="test_product_create_price_below_zero", stock=0, price=-1)

    # Test Update
    def test_product_update_normal(self):
        # Create
        product = Product.objects.create(name="test_product_update_normal", stock=100, price=100000)
        product.save()
        # Update
        product.stock = 10
        product.price = 100
        product.save()
        product_updated = Product.objects.get(name="test_product_update_normal")
        self.assertEqual(product.stock, product_updated.stock)
        self.assertEqual(product.price, product_updated.price)

    def test_product_update_stock_below_zero(self):
        # Create
        product = Product.objects.create(name="test_product_update_stock_below_zero", stock=100, price=100000)
        product.save()

        # Update
        with self.assertRaises(IntegrityError):
            product.stock = -1
            product.save()

    def test_product_update_stock_below_zero(self):
        # Create
        product = Product.objects.create(name="test_product_update_stock_below_zero", stock=100, price=100000)
        product.save()

        # Update
        with self.assertRaises(IntegrityError):
            product.price = -1
            product.save()

    # Test Delete
    def test_product_delete_normal(self):
        # Create
        product = Product.objects.create(name="test_product_delete_normal", stock=100, price=100000)
        product.save()

        # Assert Before
        self.assertEqual(1, Product.objects.count())

        # Delete
        product_deleted = Product.objects.get(name="test_product_delete_normal")
        product_deleted.delete()

        # Assert After
        self.assertEqual(0, Product.objects.count())


class ProductHistoryTestCase(TestCase):

    def test_product_history(self):
        self.assertEqual(0, FieldHistory.objects.count())
        Product.objects.create(name="test_product_history", stock=10, price=100)
        self.assertEqual(1, FieldHistory.objects.count())

        product = Product.objects.get(name="test_product_history")

        product.price = 1000
        product.save()
        self.assertEqual(2, FieldHistory.objects.count())