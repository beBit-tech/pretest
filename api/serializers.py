from rest_framework import serializers
from .models import Order, Product, OrderItem
import uuid

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock_quantity']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    class Meta:
        model = OrderItem
        fields = ['product','product_id', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ['total_price', 'created_time', 'order_items']

    def create(self, validated_data):
            order_items_data = validated_data.pop('order_items')
            order = Order.objects.create(**validated_data)

            total_price = 0
            for item_data in order_items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                total_price += product.price * quantity

            order.total_price = total_price
            order.save()

            return order