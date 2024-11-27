from django.contrib import admin
from .models import *

class orderAdmin(admin.ModelAdmin):
    readonly_fields = ['userId', 'orderNumber', 'orderDate']


class orderItemsAdmin(admin.ModelAdmin):
    readonly_fields = ['orderId', 'productID', 'productType', 'productName', 'quantity', 'price']

admin.site.register(Order, orderAdmin)
admin.site.register(OrderItems, orderItemsAdmin)
