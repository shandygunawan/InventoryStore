from django.urls import path

from . import views

app_name="igog"
urlpatterns = [
    path('dashboard/', views.dashboard, name='igog-dashboard'),
    path('incoming_create/', views.create_incoming, name="igog-incoming-create")
]