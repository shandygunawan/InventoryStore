from django.urls import path

from . import views

app_name="igog"
urlpatterns = [
    path('dashboard/', views.dashboard, name='igog-dashboard'),
    path('incomings/', views.IncomingList.as_view(), name='incoming-list'),
    path('incomings/<int:pk>/', views.IncomingDetail.as_view(), name='incoming-detail'),
    path('outgoings/', views.OutgoingList.as_view(), name='outgoing-list'),
    path('outgoings/<int:pk>/', views.OutgoingDetail.as_view(), name='outgoing-detail'),
    path('quick_account/', views.quick_account, name="igog-quickaccount"),
]