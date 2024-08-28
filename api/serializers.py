from rest_framework import serializers

from .models import Order, ProductOrder, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'amount']

class ProductOrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductOrder
        fields = ['product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductOrderSerializer(source='productorder_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id','order_number', 'total_price', 'created_time', 'products']
        read_only_fields = ['created_time']

        