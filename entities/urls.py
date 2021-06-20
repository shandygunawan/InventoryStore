from django.urls import path

from . import views

app_name="entities"
urlpatterns = [
    path('suppliers/', views.SupplierList.as_view(), name="Supplier-list"),
    path('suppliers/igog', views.SupplierIgogList.as_view(), name="supplier-incoming"),
    path('suppliers/<int:pk>', views.SupplierDetail.as_view(), name="Supplier-detail"),
    path('buyers/', views.BuyerList.as_view(), name="buyer-all"),
    path('buyers/igog', views.BuyerIgogList.as_view(), name="buyer-outgoing")
]