from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity']
    show_change_link = True  # Optional: makes product clickable

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'client_link', 'created_at', 'is_sent', 'view_items_link']
    list_filter = ['is_sent', 'created_at']
    search_fields = ['client__email', 'client__name']
    inlines = [OrderItemInline]

    def client_link(self, obj):
        url = reverse("admin:accounts_user_change", args=[obj.client.id])
        return format_html('<a href="{}">{}</a>', url, obj.client.email)
    client_link.short_description = 'Client'
    client_link.admin_order_field = 'client__email'

    def view_items_link(self, obj):
        return format_html(
            '<a href="{}">View Items</a>',
            reverse('admin:orders_order_change', args=[obj.id])
        )
    view_items_link.short_description = "Items"
