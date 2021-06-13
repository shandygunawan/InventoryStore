from django.urls import path

from . import views

app_name="entities"
urlpatterns = [
    path('suppliers/', views.get_supplier_all, name="supplier-all"),
    path('suppliers_incoming/', views.get_supplier_incoming, name="supplier-incoming"),
    path('buyers/', views.get_buyer_all, name="buyer-all")
]