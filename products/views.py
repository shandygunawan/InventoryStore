import json

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile

from rest_framework import generics, status
from rest_framework.views import APIView

from products.models import Product

class ProductListCreate(APIView):

    def get(self, request):
        try:
            products = Product.objects.all().values("id", "name", "stock", "price")
            return JsonResponse({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": None,
                "data": list(products)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            product = Product.objects.create(
                name=request.POST['name'],
                stock=request.POST['stock'],
                price=request.POST['price'],
                image=request.FILES['image']
            )
            product.save()
            return JsonResponse({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": None,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e),
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetail(APIView):
    queryset = Product.objects.all()

    def get(self, request, product_id):
        product = Product.objects.get(pk=product_id)
        price_history = product.price_history()

        res = {
            'product': {
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "image": "http://" + request.get_host() + product.image.url
            },
            'histories': list(price_history.values())
        }

        return JsonResponse({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None,
            "data": res
        }, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        # try:
            # req = json.loads(request.body)
            product = Product.objects.get(pk=product_id)

            product.name = request.POST['name']

            if product.price != request.POST['price']:
                product.price = request.POST['price']

            product.stock = request.POST['stock']

            if request.FILES.get('image', False) is not False:
                product.image = request.FILES['image']

            product.save()

            return JsonResponse({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": None
            }, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return JsonResponse({
        #         "success": False,
        #         "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         "message": str(e)
        #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return JsonResponse({
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": None
            }, safe=False)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)