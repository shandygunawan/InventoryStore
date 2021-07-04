from datetime import datetime, timedelta

from django.http import JsonResponse

from rest_framework import status

from products.models import Product
from igog.models import (
    Incoming,
    Outgoing,
    IncomingProduct,
    OutgoingProduct
)

def lowStock(request):
    threshold = request.GET.get('threshold')
    lowstock_products = Product.objects.filter(stock__lte=threshold).values('id', 'name', 'stock').order_by('stock')

    return JsonResponse({
        "success": True,
        "status_code": status.HTTP_200_OK,
        "message": "Fetch Stock Overview Successful",
        "data": list(lowstock_products)

    }, safe=False)


def highFrequencyIncoming(request):
    try:
        req_delta = request.GET.get('delta')
        req_top = request.GET.get('top')

        incomings = Incoming.objects.filter(datetime__gte=datetime.today()-timedelta(days=int(req_delta)))

        frequencies = {}
        for incoming in incomings:
            incoming_products = IncomingProduct.objects.filter(incoming=incoming)

            for incoming_product in incoming_products:
                if incoming_product.product.id in frequencies:
                    frequencies[incoming_product.product.id]['count'] += incoming_product.count
                else: # Not in
                    frequencies[incoming_product.product.id] = {
                       "name": incoming_product.product.name,
                       "count": incoming_product.count
                    }

        freqlist = []
        for freq in frequencies.items():
            freqlist.append({
                "id": freq[0],
                "name": freq[-1]['name'],
                "count": freq[-1]['count']
            })
        freqlist = sorted(freqlist, key=lambda k: k['count'], reverse=True)[:int(req_top)]

        return JsonResponse({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None,
            "data": list(freqlist)
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def highFrequencyOutgoing(request):
    try:
        req_delta = request.GET.get('delta')
        req_top = request.GET.get('top')

        outgoings = Outgoing.objects.filter(datetime__gte=datetime.today()-timedelta(days=int(req_delta)))

        frequencies = {}
        for outgoing in outgoings:
            outgoing_products = OutgoingProduct.objects.filter(outgoing=outgoing)

            for outgoing_product in outgoing_products:
                if outgoing_product.product.id in frequencies:
                    frequencies[outgoing_product.product.id]['count'] += outgoing_product.count
                else: # Not in
                    frequencies[outgoing_product.product.id] = {
                       "name": outgoing_product.product.name,
                       "count": outgoing_product.count
                    }

        freqlist = []
        for freq in frequencies.items():
            freqlist.append({
                "id": freq[0],
                "name": freq[-1]['name'],
                "count": freq[-1]['count']
            })
        freqlist = sorted(freqlist, key=lambda k: k['count'], reverse=True)[:int(req_top)]

        return JsonResponse({
            "success": True,
            "status_code": status.HTTP_200_OK,
            "message": None,
            "data": list(freqlist)
        }, safe=False)
    except Exception as e:
        return JsonResponse({
            "success": False,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)