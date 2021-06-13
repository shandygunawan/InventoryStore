import json

from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from entities.models import Supplier
from products.models import Product
from .models import Incoming, IncomingProduct



#
# UTILS
#
def toJson(chart):
    return json.dumps(list(chart.values()), cls=DjangoJSONEncoder)

def toJsonAnnotate(chart):
    return json.dumps(list(chart), cls=DjangoJSONEncoder)


#
# VIEWS
#
@csrf_exempt
def create_incoming(request):
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
            count=req_product['stock'],
            price_per_count=req_product['price']
        )
        incoming_product.save()

    return JsonResponse({
        "status": "success",
        "message": "Incoming creating successful."
    }, safe=False)

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