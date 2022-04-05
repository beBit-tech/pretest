from rest_framework import serializers

from .models import Product, Order


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['id', 'order_number', 'total_price', 'created_time']  # 'products'