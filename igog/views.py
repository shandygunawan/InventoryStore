import json

from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from entities.models import Supplier, Buyer
from products.models import Product
from .models import Incoming, IncomingProduct, Outgoing, OutgoingProduct
from igog.serializers import (
    IncomingListSerializer,
    IncomingDetailSerializer,
    OutgoingListSerializer,
    OutgoingDetailSerializer
)

#
# UTILS
#
def toJson(chart):
    return json.dumps(list(chart.values()), cls=DjangoJSONEncoder)

def toJsonAnnotate(chart):
    return json.dumps(list(chart), cls=DjangoJSONEncoder)



class IncomingList(APIView):
    queryset = Incoming.objects.all()

    def get(self, request):
        incomings = Incoming.objects.all()
        serializer = IncomingListSerializer(incomings, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            req = json.loads(request.body)
            incoming_date = datetime.strptime(req['incoming_date'], "%Y-%m-%d").date()
            incoming_time = datetime.strptime(req['incoming_time'], "%H:%M").time()
            incoming_datetime = datetime.combine(incoming_date, incoming_time)
            duedate_date = datetime.strptime(req['duedate_date'], "%Y-%m-%d").date()
            supplier = Supplier.objects.get(pk=req['supplier'])
            incoming = Incoming(
                datetime=incoming_datetime,
                payment_method=req['payment_method'],
                payment_status=req['payment_status'],
                due_date=duedate_date,
                supplier=supplier
            )
            incoming.save()

            for req_product in req['products']:
                product = Product.objects.get(pk=req_product['id'])
                incoming_product = IncomingProduct(
                    product=product,
                    incoming=incoming,
                    count=req_product['count'],
                    price_per_count=req_product['price_per_count']
                )
                incoming_product.save()

            response = {
                "success": True,
                "status_code": status.HTTP_201_CREATED,
                "message": "Incoming created"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response = {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Outgoing Created Fail"
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncomingDetail(generics.RetrieveAPIView):
    queryset = Incoming.objects.all()
    serializer_class = IncomingDetailSerializer

class OutgoingList(APIView):
    queryset = Outgoing.objects.all()

    def get(self, request):
        outgoings = Outgoing.objects.all()
        serializer = OutgoingListSerializer(outgoings, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            req = json.loads(request.body)
            outgoing_date = datetime.strptime(req['outgoing_date'], "%Y-%m-%d").date()
            outgoing_time = datetime.strptime(req['outgoing_time'], "%H:%M").time()
            outgoing_datetime = datetime.combine(outgoing_date, outgoing_time)
            duedate_date = datetime.strptime(req['duedate_date'], "%Y-%m-%d").date()
            buyer = Buyer.objects.get(pk=req['buyer'])
            outgoing = Outgoing(
                datetime=outgoing_datetime,
                payment_method=req['payment_method'],
                payment_status=req['payment_status'],
                due_date=duedate_date,
                buyer=buyer
            )
            outgoing.save()

            for req_product in req['products']:
                product = Product.objects.get(pk=req_product['id'])
                outgoing_product = OutgoingProduct(
                    product=product,
                    outgoing=outgoing,
                    count=req_product['count'],
                    price_per_count=req_product['price_per_count']
                )
                outgoing_product.save()

            response = {
                "success": True,
                "status_code": status.HTTP_201_CREATED,
                "message": "Outgoing created"
            }
            return Response(response, status=status.HTTP_201_CREATED)
        except:
            response = {
                "success": False,
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Outgoing Created Fail"
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class OutgoingDetail(generics.RetrieveAPIView):
    queryset = Outgoing.objects.all()
    serializer_class = OutgoingDetailSerializer

def dashboard(request):
    # == Queries ==
    # Chart 1
    chart1 = Incoming.objects.order_by("-total_price")[:5]

    # Chart 2
    chart2 = Incoming.objects.values('supplier_id').annotate(dcount=Count('supplier_id')).order_by('dcount')[:5]

    # Chart 3
    chart3 = Incoming.objects.filter(datetime__gte=datetime.now() - timedelta(days=5))
    # print(chart3)
    chart3 = chart3.annotate(day=TruncDate('datetime')).values('datetime').annotate(c=Count('id')).values('datetime', 'c')
    # print(chart3)

    context = {
        "chart1": toJson(chart1),
        "chart2": toJson(chart2),
        "chart3": toJsonAnnotate(chart3)
    }

    # return render(request, "igog/dashboard.html", context)
    return JsonResponse(context, safe=False)