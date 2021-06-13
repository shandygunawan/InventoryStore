from django.shortcuts import render
from entities.models import Supplier, Buyer
from django.http import JsonResponse

# Generic View
from django.views.generic.list import ListView


def get_supplier_all(request):
    suppliers = list(Supplier.objects.all().values())
    return JsonResponse(suppliers, safe=False)

def get_supplier_incoming(request):
    suppliers = list(Supplier.objects.all().values("id", "name"))
    return JsonResponse(suppliers, safe=False)

def get_buyer_all(request):
    buyers = list(Buyer.objects.all().values())
    return JsonResponse(buyers, safe=False)
