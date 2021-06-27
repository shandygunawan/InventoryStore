from django.test import TestCase
from django.db.utils import IntegrityError
from entities.models import Supplier, Buyer

#
# SUPPLIER
#
class SupplierTestCase(TestCase):
    # Test Create
    def test_supplier_create_normal(self):
        supplier = Supplier.objects.create(name="test_supplier_create_normal",
                                           phone_number="08989898797",
                                           email="test_supplier@test.com",
                                           address="Jl. Test No. 1")
        supplier.save()
        supplier_created = Supplier.objects.get(name="test_supplier_create_normal")
        self.assertEqual(supplier.name, supplier_created.name)

    def test_supplier_create_null(self):
        with self.assertRaises(IntegrityError):
            Supplier.objects.create(name="test_supplier_create_normal",
                                    phone_number=None,
                                    email="test_supplier@test.com",
                                    address="Jl. Test No. 1")


    # Test Update
    def test_supplier_update_normal(self):
        # Create
        supplier = Supplier.objects.create(name="test_supplier_update_normal",
                                           phone_number="08989898797",
                                           email="test_supplier@test.com",
                                           address="Jl. Test No. 1")
        supplier.save()
        # Update
        supplier.phone_number = '01023443'
        supplier.email = "test_supplier_update@test.com"
        supplier.save()
        supplier_updated = Supplier.objects.get(name="test_supplier_update_normal")
        self.assertEqual(supplier.phone_number, supplier_updated.phone_number)
        self.assertEqual(supplier.email, supplier_updated.email)

    # Test Delete
    def test_supplier_delete_normal(self):
        # Create
        supplier = Supplier.objects.create(name="test_supplier_delete_normal",
                                           phone_number="08989898797",
                                           email="test_supplier@test.com",
                                           address="Jl. Test No. 1")
        supplier.save()

        # Assert Before
        self.assertEqual(1, Supplier.objects.count())

        # Delete
        supplier_deleted = Supplier.objects.get(name="test_supplier_delete_normal")
        supplier_deleted.delete()

        # Assert After
        self.assertEqual(0, Supplier.objects.count())