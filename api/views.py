from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Order, Product, ProductOrder
from .serializers import OrderSerializer, ProductOrderSerializer, ProductSerializer
from .models import Order, Product, ProductOrder
from .AccessValidation import validate_token

#old validation logic
'''
def validate_token(token):
    return token == ACCEPTED_TOKEN
'''


@api_view(['POST'])
@validate_token
def import_order(request):
    order_data = request.data.copy()
    products_data = order_data.pop('products', [])
    
    order_serializer = OrderSerializer(data=order_data)
    if not order_serializer.is_valid():
        return Response(order_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        with transaction.atomic():
            order = order_serializer.save()
            
            for product_data in products_data:
                product_id = product_data.get('product_id')
                quantity = product_data.get('quantity', 1)
                
                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    # Raise an exception to trigger the transaction rollback
                    raise ValueError(f'Product with id {product_id} does not exist')
                
                ProductOrder.objects.create(order=order, product=product, quantity=quantity)
            
            # Refresh the order object to include the related products
            order.refresh_from_db()
            return Response({
                'order_id': order.id,
                'order': OrderSerializer(order).data
            }, status=status.HTTP_201_CREATED)
    except ValueError as e:
        # Catch the ValueError and return an appropriate response
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@validate_token
def get_product(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return Response(ProductSerializer(product).data)
    except Product.DoesNotExist:
        return Response({'error': f'Product with id {product_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@validate_token
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return Response(OrderSerializer(order).data)
    except Order.DoesNotExist:
        return Response({'error': f'Order with id {order_id} does not exist'}, status=status.HTTP_404_NOT_FOUND)
    
