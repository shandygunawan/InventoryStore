from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

#
# BASE CLASS
#
class BaseEntity(models.Model):
    name = models.TextField()
    phone_number = PhoneNumberField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


#
# Supplier
#
class Supplier(BaseEntity):
    email = models.EmailField()
    address = models.TextField()


#
# Buyer
#
class Buyer(BaseEntity):
    num_ktp = models.PositiveBigIntegerField()
    num_npwp = models.PositiveBigIntegerField()
