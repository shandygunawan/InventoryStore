from django.shortcuts import get_object_or_404, render, redirect, reverse
from products.models import Product
import json

# Generic View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class ProductListView(ListView):
    model = Product
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('action') == 'delete' and 'selected_products' in request.POST:
            pks = request.POST.getlist('selected_products')
            for pk in pks:
                Product.objects.filter(pk=pk).delete()

        return redirect('products:products-list')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # histories = list(product.get_price_history().values())
    histories_raw = product.get_price_history().order_by('-date_created').values()
    histories = []
    for history in histories_raw:
        histories.append({
            'price': json.loads(history['serialized_data'])[0]['fields']['price'],
            'date_created': history['date_created']
        })
    context = {
        'product': product,
        'histories': histories
    }
    return render(request, 'products/product_detail.html', context)
