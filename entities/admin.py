from django.contrib import admin
from .models import Supplier, Buyer

#
# Supplier
#
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'email', 'address')


#
# Buyer
#
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'num_ktp', 'num_npwp')


#
# Register
#
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Buyer, BuyerAdmin)