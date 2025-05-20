from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__' # ['id', 'order_number', 'total_price', 'created_at']

    def format_check(value):
        # maybe order_number format check
        pass

    order_number = serializers.CharField(required=False, validators=[format_check])


class ImportOrderSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    order = OrderSerializer(required=True)

    def create(self, validated_data):
        order = validated_data['order']
        if 'order_number' in order:
            order_number = order.pop('order_number')
            # print(f'order_number {order_number}')
            validated_data['order'], _ = Order.objects.update_or_create(order_number=order_number, defaults=order)
        else:
            validated_data['order'] = Order.objects.create(**order)
        
        return validated_data