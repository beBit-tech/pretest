from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from functools import wraps
from django.db import transaction

ACCEPTED_TOKEN = 'omni_pretest_token'

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header != ACCEPTED_TOKEN:
            return Response({"error": "Invalid token"}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@api_view(['POST'])
@token_required
@transaction.atomic 
def import_order(request):
    # Parse data
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"error": serializer.errors}, status=400)

    # Save order to the database
    order = serializer.save()

    # Return success response with total_price
    return Response({
        "message": "Order imported successfully",
        "order_id": order.id,
        "total_price": order.total_price
    }, status=201)