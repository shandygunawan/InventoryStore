from django.contrib import admin
from .models import Incoming, IncomingProduct, IncomingDeliveryNote

class IncomingProductInline(admin.TabularInline):
    model = IncomingProduct
    extra = 1

class IncomingAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'total_price', 'payment_type', 'payment_status', 'due_date')
    inlines = [IncomingProductInline]

class IncomingDeliveryNoteAdmin(admin.ModelAdmin):
    list_display = ('date', 'retrieval_type')


# Register
admin.site.register(Incoming, IncomingAdmin)
admin.site.register(IncomingDeliveryNote, IncomingDeliveryNoteAdmin)
