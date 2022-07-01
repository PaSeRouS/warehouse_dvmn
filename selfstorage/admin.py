from django.contrib import admin

from .models import Box, Customer, Order
from .models import Size, Warehouse


class WarehouseBoxInline(admin.TabularInline):
    model = Box

class CustomerBoxInline(admin.TabularInline):
    model = Box
    fields = ('name', 'warehouse')

@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    inlines = [
        WarehouseBoxInline,
    ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [
        CustomerBoxInline,
    ]

admin.site.register(Box)
# admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Size)