from django.urls import path

# Generic Views
# from products.views import ProductListView
from . import views

app_name='products'
urlpatterns = [
    path('', views.ProductListCreate.as_view(), name="product-list"),
    path(r'<int:product_id>/', views.ProductDetail.as_view(), name='products-detail'),
]