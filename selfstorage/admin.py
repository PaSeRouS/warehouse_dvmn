from django.contrib import admin

from .models import Box, Customer, Order
from .models import Size, Warehouse

admin.site.register(Box)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Size)
admin.site.register(Warehouse)