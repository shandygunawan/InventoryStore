from django.contrib import admin
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'role', 'phone_number', 'address', 'salary', 'created_at')

admin.site.register(User, UserAdmin)