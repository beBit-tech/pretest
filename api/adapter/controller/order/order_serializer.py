from rest_framework import serializers

class OrderLineSerializer(serializers.Serializer):
    product_number = serializers.CharField(max_length = 100, required = True)
    quantity = serializers.IntegerField(min_value = 1, required = True)

class OrderSerializer(serializers.Serializer):
    total_price = serializers.FloatField(required = True)
    created_time = serializers.DateTimeField(required = True)
    order_lines = OrderLineSerializer(many = True)

    def validate(self, data):
        if data['total_price'] <= 0:
            raise serializers.ValidationError("Total price must be greater than 0")
        return data