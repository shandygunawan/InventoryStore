from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'image', 'created_at', 'updated_at')


admin.site.register(Product, ProductAdmin)
