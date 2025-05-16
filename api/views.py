from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from .models import Order
from django.http import JsonResponse

# Validate access token from request data
# ( accepted token is defined in api/views.py )
# Parse data and Save to corresponding fields


ACCEPTED_TOKEN = ('omni_pretest_token')

@api_view(['POST'])
def import_order(request):
    # Validate access token from request data
    token = request.data.get('access_token')
    if token != ACCEPTED_TOKEN:
        return JsonResponse({'Error!': 'Invalid Token'}, status=403)
    
    # Parse corresponding fields data
    order_number = request.data.get('order_number')
    total_price = request.data.get('total_price')

    if not order_number or not total_price:
        return JsonResponse({'Error!': 'Missing Data'}, status=400)
    
    try:
        # Save data
        order = Order.objects.create(
            order_number =  order_number,
            total_price = total_price
        )
        return JsonResponse({
            'Message': 'Order Created!',
            'order_id': order.id
        }, status=201)
    
    except Exception as e:
        return JsonResponse({'Error!': str(e)}, status=500)
