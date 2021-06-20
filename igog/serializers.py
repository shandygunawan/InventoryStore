import json
from datetime import datetime, timedelta

from rest_framework import serializers

from igog.models import Incoming, IncomingProduct, Outgoing, OutgoingProduct
from products.serializers import ProductSerializer
from entities.models import Supplier
from products.models import Product
from entities.serializers import SupplierSerializer, BuyerSerializer


class IgogProductSerializer(serializers.ModelSerializer):
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
    products = IgogProductSerializer(source="incomingproduct_set", many=True)
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Incoming
        fields = ['id', 'datetime', 'payment_method', 'payment_status', 'due_date', 'supplier', 'products']


class OutgoingListSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.name')

    class Meta:
        model = Outgoing
        fields = ['id', 'datetime', 'payment_method', 'payment_status', 'due_date', 'buyer_name']


class OutgoingDetailSerializer(serializers.ModelSerializer):
    products = IgogProductSerializer(source="outgoingproduct_set", many=True)
    buyer = BuyerSerializer(read_only=True)

    class Meta:
        model = Outgoing
        fields = ['id', 'datetime', 'payment_method', 'payment_status', 'due_date', 'buyer', 'products']