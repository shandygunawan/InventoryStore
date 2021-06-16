from rest_framework import generics

from entities.models import Supplier, Buyer
from entities.serializers import SupplierSerializer, BuyerSerializer


class SupplierList(generics.ListCreateAPIView):
    """
    List all supplier, or create a new supplier.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class SupplierDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a supplier instance
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class BuyerList(generics.ListCreateAPIView):
    """
    List all buyer, or create a new buyer.
    """
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer

class BuyerDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, Update or delete a buyer instance
    """
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer