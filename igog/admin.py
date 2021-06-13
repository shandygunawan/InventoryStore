from django.contrib import admin
from .models import *

#
# INCOMING
#
class IncomingProductInline(admin.TabularInline):
    model = IncomingProduct
    extra = 1

class IncomingAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'payment_method', 'payment_status', 'due_date')
    inlines = [IncomingProductInline]

class IncomingDeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('date', 'retrieval_type')


#
# OUTGOING
#
class OutgoingProductInline(admin.TabularInline):
    model = OutgoingProduct
    extra = 1

class OutgoingAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'payment_method', 'payment_status', 'due_date')
    inlines = [OutgoingProductInline]

class OutgoingDeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('date', 'retrieval_type')


# Register
admin.site.register(Incoming, IncomingAdmin)
admin.site.register(IncomingDeliveryNote, IncomingDeliveryNoteAdmin)
admin.site.register(Outgoing, OutgoingAdmin)
admin.site.register(OutgoingDeliveryNote, OutgoingDeliveryNoteAdmin)
