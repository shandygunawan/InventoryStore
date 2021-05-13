from django.db import models
from field_history.tracker import FieldHistoryTracker

class Product(models.Model):
    name = models.TextField(blank=False, unique=False, null=False)
    stock = models.PositiveBigIntegerField(default=0, blank=False, null=False)
    price = models.PositiveBigIntegerField(default=0, blank=False, null=False)
    image = models.ImageField(default="products_default.jpg", upload_to='products_images')

    price_history = FieldHistoryTracker(['price'])

    def __str__(self):
        return self.name