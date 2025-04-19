from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
from .decorators import api_token_required
from .validators import OrderValidator
import json
from decimal import Decimal

# Create your views here.
@api_view(['POST'])
@api_token_required
def import_order(request):
    data = json.loads(request.body)
    
    is_valid, error_response = OrderValidator.validate(data)
    
    if not is_valid:
        return error_response
    
    order_number = data.get('order_number')
    total_price = Decimal(data.get('total_price'))
    
    try:
        order = Order.objects.create(
            order_number=order_number,
            total_price=total_price
        )
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return JsonResponse({
        'success': True,
        'order_id': order.id,
        'order_number': order.order_number,
        'total_price': Decimal(order.total_price),
        'created_time': order.created_time
    }, status=status.HTTP_201_CREATED)
        