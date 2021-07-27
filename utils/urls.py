from django.urls import path

# Generic Views
# from products.views import ProductListView
from . import views

app_name='utils'
urlpatterns = [
    path('checkhealth/', views.checkHealth, name="utils-checkhealth"),
    path('backup/list/', views.listBackupDropbox, name='utils-backuplist'),
    path('backup/create/', views.backupDb, name="utils-backupcreate"),
    path('backup/info/', views.backupInfo, name="utils-backupinfo")
]