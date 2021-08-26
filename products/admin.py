from django.contrib import admin
from .models import Product, ProductPriceHistory


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'image', 'created_at', 'updated_at')

class ProductPriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("product", "created_at", "price")

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductPriceHistory, ProductPriceHistoryAdmin)