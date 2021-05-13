from django.shortcuts import get_object_or_404, render
from products.models import Product

# Generic View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class ProductListView(ListView):
    model = Product
    paginate_by = 10

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
