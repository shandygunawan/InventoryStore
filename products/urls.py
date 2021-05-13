from django.urls import path

# Generic Views
from products.views import ProductListView
from . import views

app_name='products'
urlpatterns = [
    path('', ProductListView.as_view(), name='products-list'),
    path(r'<int:product_id>/', views.detail, name='products-detail')
]