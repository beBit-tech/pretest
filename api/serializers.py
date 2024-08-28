from rest_framework import serializers

from .models import Order, ProductOrder, Product

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'total_price', 'created_time']
        read_only_fields = ['created_time']

        