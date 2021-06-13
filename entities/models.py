from django.db import models

#
# BASE CLASS
#
class BaseEntity(models.Model):
    name = models.TextField()
    phone_number = models.PositiveBigIntegerField()

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
