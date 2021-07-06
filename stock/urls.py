from django.urls import path

from . import views

app_name="stock"
urlpatterns = [
    path('low_stock', views.lowStock, name="stock-lowstock"),
    path('highfrequency/incoming', views.highFrequencyIncoming, name="stock-highfrequency-incoming"),
    path('highfrequency/outgoing', views.highFrequencyOutgoing, name="stock-highfrequency-outgoing"),
    path('productSoldperDay', views.productSoldperDay, name="stock-productsoldperday")
]