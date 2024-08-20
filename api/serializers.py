from rest_framework import serializers

from .models import Customer, Order, OrderProduct, Product


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ["id", "username", "email"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "quantity"]


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderProduct
        fields = ["product", "quatity"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderProductSerializer(many=True, read_only=True)
    customer = serializers.SlugRelatedField(
        queryset=Customer.objects.all(), slug_field="username"
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "order_number",
            "total_price",
            "created_time",
            "customer",
            "items",
        ]
        read_only_fields = ["created_time"]
