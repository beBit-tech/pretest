from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    # Check if token is provided and valid
    token = request.data.get('token')
    
    if not token or token != ACCEPTED_TOKEN:
        return JsonResponse(
            {'error': 'Invalid or missing token'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    order_number = request.data.get('order_number')
    total_price = request.data.get('total_price')

    # Validate order_number and total_price
    if not order_number or not total_price:
        return JsonResponse(
            {'error': 'Missing order_number or total_price'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Validate data types
    try:
        total_price = float(total_price)
    except (ValueError, TypeError):
        return JsonResponse(
            {'error': 'total_price must be a number'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Create the order
    try:
        order = Order.objects.create(
            order_number=order_number,
            total_price=total_price
        )
        
        return JsonResponse({
            'order_number': order.order_number,
            'total_price': float(order.total_price),
            'created_time': order.created_time
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Handle duplicate order_number
        if 'unique constraint' in str(e).lower():
            return JsonResponse(
                {'error': 'Order number already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        # Handle other exceptions
        return JsonResponse(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )