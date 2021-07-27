from django.contrib import admin
from .models import GlobalConfig

# Register your models here.
class GlobalConfigAdmin(admin.ModelAdmin):
    list_display = ("key", "value")

admin.site.register(GlobalConfig, GlobalConfigAdmin)