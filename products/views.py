import json

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.fields.files import ImageFieldFile

from products.models import Product


class ImageFieldEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, ImageFieldFile):
            return str(o)
        else:
            return super().default(o)


def get_all(request):
    products = list(Product.objects.all().values("id", "name", "stock", "price"))
    return JsonResponse(products, safe=False)

def get_detail(request, product_id):
    product = Product.objects.get(pk=product_id)
    histories_raw = product.get_price_history().order_by('-date_created').values()
    histories = []
    for history in histories_raw:
        histories.append({
            'price': json.loads(history['serialized_data'])[0]['fields']['price'],
            'date_created': history['date_created']
        })
    to_return = {
        'product': {
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "image": product.image.url
        },
        'histories': histories
    }
    return JsonResponse(to_return, safe=False)