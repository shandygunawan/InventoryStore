from django.urls import path

# Generic Views
# from products.views import ProductListView
from . import views

app_name='products'
urlpatterns = [
    # path('', ProductListView.as_view(), name='products-list'),
    path('', views.get_all, name='products-all'),
    path(r'<int:product_id>/', views.get_detail, name='products-detail'),
]