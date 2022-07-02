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

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at']

admin.site.register(Box)
# admin.site.register(Order)
admin.site.register(Size)