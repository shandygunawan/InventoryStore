from django.urls import path

from . import views

app_name="igog"
urlpatterns = [
    path('dashboard/', views.dashboard, name='igog-dashboard'),
    path('incomings/', views.IncomingList.as_view(), name='incoming-list'),
    path('incomings/<int:pk>/', views.IncomingDetail.as_view(), name='incoming-detail'),
    # path('incoming_create/', views.create_incoming, name="igog-incoming-create")
]