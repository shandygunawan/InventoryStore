import json

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile

from rest_framework import generics
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductSerializer

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(APIView):
    queryset = Product.objects.all()

    def get(self, request, product_id, format=None):
        product = Product.objects.get(pk=product_id)
        histories_raw = product.get_price_history().order_by('-date_created').values()
        histories = []
        for history in histories_raw:
            histories.append({
                'price': json.loads(history['serialized_data'])[0]['fields']['price'],
                'date_created': history['date_created']
            })
        res = {
            'product': {
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "image": "http://localhost:8000" + product.image.url
            },
            'histories': histories
        }
        return JsonResponse(res, safe=False)