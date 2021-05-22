from django.urls import path

from . import views

app_name="igog"
urlpatterns = [
    path('dashboard/', views.dashboard, name='igog-dashboard')
]