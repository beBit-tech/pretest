from rest_framework import serializers
from .models import Order
from .models import Product

class Orderserializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields= ['Order_number', 'Total_price', 'Created_time', 'Detail', 'product'] 

class Productserializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields= ['Product_name','Product_price','Product_genre'] 