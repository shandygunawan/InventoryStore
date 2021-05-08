from django.db import models


class Product(models.Model):
    name = models.TextField(blank=False, unique=False, null=False)
    stock = models.PositiveBigIntegerField(blank=False, null=False)

    def __str__(self):
        return self.name
