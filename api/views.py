from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order

ACCEPTED_TOKEN = 'omni_pretest_token'

@api_view(['POST'])
def import_order(request):
    # Validate access token
    auth_header = request.headers.get('Authorization')
    if auth_header != ACCEPTED_TOKEN:
        return Response({"error": "Invalid token"}, status=401)

    # Parse data
    order_data = request.data
    if not order_data:
        return Response({"error": "No order data provided"}, status=400)

    # Save order to the database
    try:
        order = Order.objects.create(**order_data)
    except Exception as e:
        return Response({"error": f"Error saving order: {str(e)}"}, status=400)

    # Return success response with total_price
    return Response({
        "message": "Order imported successfully",
        "order_id": order.id,
        "total_price": order.total_price
    }, status=201)