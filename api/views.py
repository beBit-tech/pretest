from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
import json

# Create your views here.

ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')
        
        if token != ACCEPTED_TOKEN:
            return JsonResponse({'error': 'Invalid access token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        order_number = data.get('order_number')
        total_price = data.get('total_price')
        
        if not order_number or not total_price:
            return JsonResponse({'error': 'Order number and total price cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(
            order_number=order_number,
            total_price=total_price
        )
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'order_number': order.order_number,
            'total_price': order.total_price,
            'created_time': order.created_time
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)