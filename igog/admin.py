from django.contrib import admin
from .models import *


#
# INCOMING
#
class IncomingProductInline(admin.TabularInline):
    model = IncomingProduct
    extra = 1


class IncomingAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'delivery_note', 'price_total',
                    'datetime', 'supplier', 'payment_method',
                    'installment_tenor', 'installment_paid', 'installment_duedate',
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
    list_display = ('invoice', 'delivery_note', 'price_total',
                    'datetime', 'buyer', 'payment_method',
                    'installment_tenor', 'installment_paid', 'installment_duedate',
                    'retrieval_type', 'retrieval_date',
                    'created_at', 'updated_at')
    inlines = [OutgoingProductInline]


# Register
admin.site.register(Incoming, IncomingAdmin)
admin.site.register(Outgoing, OutgoingAdmin)
