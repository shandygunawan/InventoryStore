from django.contrib import admin
from .models import *


#
# INCOMING
#
class IncomingProductInline(admin.TabularInline):
    model = IncomingProduct
    extra = 1


class IncomingAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'delivery_note', 'datetime',
                    'supplier', 'payment_method', 'payment_status',
                    'installment_duedate', 'installment_fee',
                    'retrieval_type', 'retrieval_date',
                    'created_at', 'updated_at')
    inlines = [IncomingProductInline]


#
# OUTGOING
#
class OutgoingProductInline(admin.TabularInline):
    model = OutgoingProduct
    extra = 1


class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'delivery_note', 'datetime',
                    'buyer', 'payment_method', 'payment_status',
                    'installment_duedate', 'installment_fee',
                    'retrieval_type', 'retrieval_date',
                    'created_at', 'updated_at')
    inlines = [OutgoingProductInline]


# Register
admin.site.register(Incoming, IncomingAdmin)
admin.site.register(Outgoing, OutgoingAdmin)
