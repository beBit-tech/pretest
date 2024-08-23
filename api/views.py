from django.http import JsonResponse, HttpResponseBadRequest
from rest_framework.decorators import api_view
from .models import Order
from .decorators import validate_token

@api_view(['POST'])
@validate_token
def import_order(request):
    order_number = request.data.get('order_number')
    total_price = request.data.get('total_price')
    
    if not order_number or not total_price:
        return HttpResponseBadRequest("Missing required fields")

    try:
        order = Order(order_number=order_number, total_price=total_price)
        order.save()
        return JsonResponse({"message": "Order created successfully", "order_id": order.id})
    except Exception as e:
        return HttpResponseBadRequest(f"An error occurred: {str(e)}")