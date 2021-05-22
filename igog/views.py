from datetime import datetime, timedelta
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render
from .models import Incoming
import json

def toJson(chart):
    return json.dumps(list(chart.values()), cls=DjangoJSONEncoder)

def toJsonAnnotate(chart):
    return json.dumps(list(chart), cls=DjangoJSONEncoder)

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

    return render(request, "igog/dashboard.html", context)
