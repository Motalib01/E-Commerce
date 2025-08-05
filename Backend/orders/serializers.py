# pylint: disable=no-member

from rest_framework import serializers
from .models import Order, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'client', 'created_at', 'is_sent', 'items']
        read_only_fields = ['id', 'created_at', 'is_sent', 'client']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(client=user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
