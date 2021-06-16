from django.urls import path

from . import views

app_name="entities"
urlpatterns = [
    path('suppliers/', views.SupplierList.as_view(), name="Supplier-list"),
    path('suppliers/<int:pk>', views.SupplierDetail.as_view(), name="Supplier-detail"),
    path('buyers/', views.BuyerList.as_view(), name="buyer-all")
]