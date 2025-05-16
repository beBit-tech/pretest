from datetime import datetime
from inspect import stack
from itertools import product
from os import name
from rest_framework import serializers


'''DRF print data: json format'''


class OrderSerializer(serializers.Serializer):
    order_num = serializers.IntegerField()
    total_price = serializers.IntegerField()
    created = serializers.DateTimeField


class CommentSeriallizer(serializers.Serializer):
    content = serializers.CharField()
    create_time = serializers.DateTimeField(
        format="%Y-%m-%d"
    )
    buyuser = serializers.CharField()



class SellerSeriallizer(serializers.Serializer):
    buyeruser = serializers.SerializerMethodField()
    store_name = serializers.CharField()


    def get_buyeruser(self, obj):
        if obj.buyeruser:
            return obj.buyeruser.name
        return None 





class ProductSeriallizer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()
    stack = serializers.IntegerField()
    descript = serializers.CharField()
    
    seller = serializers.SerializerMethodField()

    def get_seller(self,obj):
        return obj.seller.buyeruser.name


class ProductSellSeriallizer(serializers.Serializer):
    product = serializers.SerializerMethodField()
    sell_num = serializers.IntegerField()

    def get_product(self,obj):
        return obj.product.name
