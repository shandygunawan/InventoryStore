import os.path

from django.core.files.storage import FileSystemStorage
from django.db import models
from field_history.tracker import FieldHistoryTracker

from InventoryStore.settings import MEDIA_ROOT

# So no duplicate when using the same image for product
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(MEDIA_ROOT, name))
        return name


class ProductPriceHistory(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    price = models.PositiveBigIntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        unique_together = ('product', 'created_at')

    def save(self, *args, **kwargs):
        super(ProductPriceHistory, self).save(*args, **kwargs)


class Product(models.Model):
    name = models.TextField(blank=False, unique=False, null=False)
    stock = models.PositiveBigIntegerField(default=0, blank=False, null=False)
    price = models.PositiveBigIntegerField(default=0, blank=False, null=False)
    image = models.ImageField(default="placeholders/products.jpg", upload_to='products_images', storage=OverwriteStorage())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def price_history(self):
        return ProductPriceHistory.objects.filter(product=self).order_by('-created_at')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)

        # save price history
        price_history = self.price_history()
        if not price_history or int(self.price) != price_history[0].price:
            new_price = ProductPriceHistory(product=self, price=self.price)
            new_price.save()
