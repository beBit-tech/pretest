from rest_framework import serializers,exceptions
from .models import Order,ProductOrder,Product
from decimal import Decimal
import uuid

class OrderSerializer(serializers.ModelSerializer):  
    '''Normal Model Serialzer for Order'''
    class Meta:
        model=Order
        fields = (
            'order_number',
            'total_price',
            'buyer',            
            'created_time',
            'last_update',
            'quantity'
        )
class OrderDetailSerializer(serializers.ModelSerializer):  
    '''Custom Model Serialzer to show Order detail'''
    class Meta:
        model=ProductOrder
        fields =('order','product','quantity')

    def to_representation(self, instance):
        data = super(OrderDetailSerializer, self).to_representation(instance)
        data['product']={
            "number":data['product'],
            "title":Product.objects.get(product_number=data['product']).title,
            "quantity":data.pop('quantity')
        }        
        return {
            "Products":data['product']
        }
   
class NestedOrderSerializer(serializers.Serializer):
    '''
    Check taht the nested data(Products_data) in OrderImportSerializer is valid
    '''
    product_number = serializers.UUIDField(allow_null=False)
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_number(self,value):
        if Product.objects.filter(pk=value).exists()==False:
            raise serializers.ValidationError(f"({value}) does not exist")
        if Product.objects.get(pk=value).status==False:
            raise serializers.ValidationError(f"({value}) is not available")
        return value    

    def validate(self,data):
        '''validate the required quantity is availible'''
        if Product.objects.get(pk=data['product_number']).quantity<data['quantity']:
            raise serializers.ValidationError("SORRY! The Product is out of stock")
        return data

class OrderImportSerializer(serializers.Serializer): 
    """Custom Serializer to handle Order Import (PUT and POST)"""
    def to_internal_value(self, data):
        initial_data=self.initial_data
        try:
            products_data = initial_data.pop('products_data')
        except:
            raise exceptions.ParseError({"error":["field [products_data] is neccessary"]})
        try:
            buyer = initial_data.pop('buyer')
        except:
            raise exceptions.ParseError({"error":["field [buyer] is neccessary"]})
        
        serializer=NestedOrderSerializer(data=products_data,many=True)

        if not serializer.is_valid():
            print(type(serializer.errors))
            raise exceptions.ParseError(f"{serializer.errors}")
        quantity = len(products_data)
        total_price=0
        for product in products_data:
            try:
                p = Product.objects.get(pk=uuid.UUID(product['product_number']))
            except Product.DoesNotExist:
                raise exceptions.ParseError("Product Model does not exist")
            except:
                raise exceptions.ParseError("The given product_number does not exist")
            if product['quantity'] <=0:
                raise exceptions.ParseError(f"{p.title}({p.product_number}) : Quantity is wrong")
            product['product']=p
            total_price+=p.price*product['quantity']

        return {
            'total_price': Decimal(total_price),
            'buyer': buyer,
            'quantity':quantity,
            'products_data':products_data
        }
    def update(self, instance, validated_data):
        # get the old order 
        order = instance
        # update with new PUT data
        order.total_price=validated_data.get('total_price',order.total_price)
        order.buyer=validated_data.get('buyer',order.buyer)
        order.quantity=validated_data.get('quantity',order.quantity)
        #Delete the old ProductOrder and Create new ProductOrder for this order
        products_data=validated_data.pop('products_data')  
        #Update Product Model
        previous_productorder=order.orders.all()
        for productorder in previous_productorder:
            product=productorder.product
            product.quantity += productorder.quantity
            product.save()
        #Update Product Order Model
        previous_productorder.delete()
        for product in products_data:
            ProductOrder.objects.create(order=order,product=product['product'],quantity=product['quantity'])
            product['product'].quantity-= product['quantity']
            product['product'].save()
            
        validated_data = OrderSerializer(order)
        order.save()
        return validated_data.data
        

    def create(self,validated_data):    
        products_data=validated_data.pop('products_data')    
        order = Order.objects.create(**validated_data)
        for product in products_data:
            #update productOrder model
            ProductOrder.objects.create(order=order,product=product['product'],quantity=product['quantity'])
            #update product model
            product['product'].quantity-= product['quantity']
            product['product'].save()
        validated_data = OrderSerializer(order)
        return validated_data.data


class ProductSerializer(serializers.ModelSerializer): 
    quantity = serializers.IntegerField(min_value=1) 
    '''Normal Model Serializer for Product'''
    class Meta:
        model=Product
        fields = (
            'product_number',
            'title',
            'price',
            'quantity',
            'status',
        )  

