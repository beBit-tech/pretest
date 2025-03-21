from rest_framework import serializers

from django.db import transaction

from .models import Order, OrderItem, Product

class OrderItemSerializer(serializers.Serializer):
    """
    Serializer for OrderItem model.
    Request fields: 
        - quantity
        - product_title
    Response fields: 
        - quantity
        - product_title
        - price_at_purchase
    """
    quantity = serializers.IntegerField(min_value=1, required=True)
    product_title = serializers.CharField(required=True)

    price_at_purchase = serializers.FloatField(read_only=True)

    def validate(self, data: dict):
        """Validates that the product exists and the quantity is less than or equal to the inventory."""
        product_title = data.get("product_title")
        quantity = data.get("quantity")

        try:
            product = Product.objects.get(title=product_title)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with title {product_title} does not exist.")

        if quantity > product.inventory:
            raise serializers.ValidationError(f"Quantity must be less than or equal to the inventory of the {product_title}.")
        return data
    

class OrderSerializer(serializers.Serializer):
    """
    Serializer for Order model.
    Request fields:
        - order_items: [OrderItem Model, OrderItem Model, ...]
    Response fields:
        - order_number
        - created_at
        - total_price
        - status
        - order_items: [OrderItem Model, OrderItem Model, ...]
    """
    order_items = OrderItemSerializer(many=True,required=True)
    order_number = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    status = serializers.CharField(read_only=True, source="get_status_display")

    def validate_order_items(self, value: list):
        """order_items can"t be empty"""
        if not value:
            raise serializers.ValidationError("order_items can't be empty")
        return value
    
    def create(self, validated_data: dict):
        """
        Create Order and OrderItems in a transaction.
        Calculate total price and update product inventory.
        """
        order_items_data = validated_data.pop("order_items")
        total_price = 0

        with transaction.atomic():
            order = Order.objects.create(total_price=total_price)

            for item in order_items_data:
                product = Product.objects.get(title=item["product_title"])
                quantity = item["quantity"]
                OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=quantity,
                    price_at_purchase=product.price,
                    product_title=product.title
                )
                total_price += product.price * quantity
                product.inventory -= quantity
                product.save()

            order.total_price = total_price
            order.save()

        return order
    

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model.
    Request & Response fields:
        - title
        - price
        - inventory
    """
    class Meta:
        model = Product
        fields = ["title", "price", "inventory"]

    def validate_price(self, value: float):
        if value < 1:
            raise serializers.ValidationError("Price cannot be negative.")
        return value

    def validate_inventory(self, value: int):
        if value < 0:
            raise serializers.ValidationError("Inventory cannot be negative.")
        return value