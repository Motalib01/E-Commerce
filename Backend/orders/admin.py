from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'client_name', 'client_email', 'client_city', 'created_at', 'is_confirmed', 'total_amount'
    )
    list_filter = ('is_confirmed', 'client_city')
    search_fields = ('client_name', 'client_email')
    readonly_fields = ('total_amount',)
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)
