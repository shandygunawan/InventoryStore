import json
from datetime import datetime, timedelta

from rest_framework import serializers

from igog.models import Incoming, IncomingProduct
from products.serializers import ProductSerializer
from entities.models import Supplier
from products.models import Product
from entities.serializers import SupplierSerializer

class IncomingProductSerializer(serializers.ModelSerializer):
    product = serializers.ReadOnlyField(source="product.name")

    class Meta:
        model = IncomingProduct
        fields = ['product', 'count', "price_per_count"]

class IncomingListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name')

    class Meta:
        model = Incoming
        fields = ['id', 'datetime', 'payment_method', 'payment_status', 'due_date', 'supplier_name']

class IncomingDetailSerializer(serializers.ModelSerializer):
    products = IncomingProductSerializer(source="incomingproduct_set", many=True)
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Incoming
        fields = ['id', 'datetime', 'payment_method', 'payment_status', 'due_date', 'supplier', 'products']

# class IncomingCreateSerializer(serializers.ModelSerializer):
#     incoming = IncomingDetailSerializer(many=True)
#     products = IncomingProductSerializer(many=True)
#
#     class Meta:
#         model = Incoming
#         fields = "__all__"
#
#     def create(self, validated_data):
#         print(validated_data)