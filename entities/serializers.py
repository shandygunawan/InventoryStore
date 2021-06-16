from rest_framework import serializers

from entities.models import Supplier, Buyer

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone_number', 'email', 'address']

class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ['id', 'name', 'phone_number', 'num_ktp', 'num_npwp']