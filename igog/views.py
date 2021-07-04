import json

from datetime import datetime, timedelta
from django.db.models import Count, F, Sum
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse

from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from entities.models import Supplier, Buyer
from products.models import Product
from igog.models import (
    BaseIgog,
    Incoming,
    IncomingProduct,
    Outgoing,
    OutgoingProduct
)
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


#
# CRUD
#

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
            installment_duedate = datetime.strptime(req['installment_duedate'], "%Y-%m-%d").date()
            supplier = Supplier.objects.get(pk=req['supplier'])
            incoming = Incoming(
                invoice=req['invoice'],
                delivery_note=req['delivery_note'],
                price_total=0,
                datetime=incoming_datetime,
                payment_method=req['payment_method'],
                installment_duedate=installment_duedate,
                installment_tenor=req['installment_tenor'],
                installment_paid=req['installment_paid'],
                retrieval_type=req['retrieval_type'],
                note=req['note'],
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
        except Exception as e:
            print(e)
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
            installment_duedate = datetime.strptime(req['installment_duedate'], "%Y-%m-%d").date()
            buyer = Buyer.objects.get(pk=req['buyer'])
            outgoing = Outgoing(
                invoice=req['invoice'],
                delivery_note=req['delivery_note'],
                price_total=0,
                datetime=outgoing_datetime,
                payment_method=req['payment_method'],
                installment_duedate=installment_duedate,
                installment_tenor=req['installment_tenor'],
                installment_paid=req['installment_paid'],
                retrieval_type=req['retrieval_type'],
                note=req['note'],
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
        except Exception as e:
            print(e)
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

#
# FINANCE
#
def finance(request):
    # Quick Account
    qa_incoming_sum = 0
    for incoming in Incoming.objects.filter(installment_paid__lt=F('installment_tenor')):
        qa_incoming_sum += incoming.price_total

    qa_outgoing_sum = 0
    for outgoing in Outgoing.objects.filter(installment_paid__lt=F('installment_tenor')):
        qa_outgoing_sum += outgoing.price_total

    # Incoming Prices per day in last week
    incoming_last7days = Incoming.objects\
        .filter(datetime__gte=datetime.today()-timedelta(days=7))\
        .annotate(datetime_date=TruncDate('datetime'))\
        .values('datetime_date')\
        .annotate(total=Sum('price_total'))\
        .order_by('datetime_date')

    # Outgoing Prices per day in last week
    outgoing_last7days = Outgoing.objects \
        .filter(datetime__gte=datetime.today() - timedelta(days=7)) \
        .annotate(datetime_date=TruncDate('datetime')) \
        .values('datetime_date') \
        .annotate(total=Sum('price_total'))\
        .order_by('datetime_date')

    # Number of payable almost finished (2 months)
    payable_almost = 0
    payable = Incoming.objects.filter(installment_paid__lt=F('installment_tenor'))
    payable_num = payable.count()
    for incoming in payable:
        if incoming.installment_tenor - incoming.installment_paid == 1:
            payable_almost += 1

    # Top 10 products Sold
    topproducts = []
    for product in Product.objects.all():
        outgoing_products = OutgoingProduct.objects.filter(product=product)
        product_price_total = 0
        for outgoing_product in outgoing_products:
            product_price_total += (outgoing_product.count * outgoing_product.price_per_count)

        topproducts.append({
            "id": product.id,
            "name": product.name,
            "total_price": product_price_total
        })
    topproducts = sorted(topproducts, key=lambda k: k['total_price'], reverse=True)[:10]

    # Top 10 outgoings
    topoutgoings = []
    for outgoing in Outgoing.objects.order_by("-price_total")[:10]:
        topoutgoings.append({
            "id": outgoing.id,
            "invoice": outgoing.invoice,
            "total_price": outgoing.price_total
        })

    # Top 10 suppliers
    topsuppliers = []
    for supplier in Supplier.objects.all():
        incomings = Incoming.objects.filter(supplier=supplier)
        supplier_price_total = 0
        for incoming in incomings:
            supplier_price_total += incoming.price_total
        topsuppliers.append({
            "id": supplier.id,
            "name": supplier.name,
            "total_price": supplier_price_total
        })
    topsuppliers = sorted(topsuppliers, key=lambda k: k['total_price'], reverse=True)[:10]

    # Top 10 Buyers
    topbuyers = []
    for buyer in Buyer.objects.all():
        outgoings = Outgoing.objects.filter(buyer=buyer)
        buyer_price_total = 0
        for outgoing in outgoings:
            buyer_price_total += outgoing.price_total
        topbuyers.append({
            "id": buyer.id,
            "name": buyer.name,
            "total_price": buyer_price_total
        })
    topbuyers = sorted(topbuyers, key=lambda k: k['total_price'], reverse=True)[:10]

    return JsonResponse({
        "quick_account": {
            "incoming_sum": qa_incoming_sum,
            "outgoing_sum": qa_outgoing_sum
        },
        "incoming_7days": list(incoming_last7days),
        "outgoing_7days": list(outgoing_last7days),
        "payable_almost": {
            "almost": payable_almost,
            "num": payable_num
        },
        "topproducts": topproducts,
        "topoutgoings": topoutgoings,
        "topsuppliers": topsuppliers,
        "topbuyers": topbuyers
    }, safe=False)
