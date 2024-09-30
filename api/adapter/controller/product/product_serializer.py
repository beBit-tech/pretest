from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255, required=True)
    price = serializers.FloatField(required=True)

    def validate(self, data):
        if 'price' in data and data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return data