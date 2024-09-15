from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['order_number', 'total_price']
    
    def validate_total_price(self, value):
        if value < 0:
            raise serializers.ValidationError("total_price must be a positive number.")
        return value