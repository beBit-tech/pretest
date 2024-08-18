from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order
from .serializers import OrderSerializer

# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')

def validate_token(token):
    return token == ACCEPTED_TOKEN


@api_view(['POST'])
def import_order(request):
    # Extract the token from the request headers
    token = request.headers.get('Authorization')

    # Validate the extracted token
    if not validate_token(token):
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Parse the data from request using serializer
    serializer = OrderSerializer(data=request.data)

    # Validate the data
    if serializer.is_valid():
        # save the valid data
        order = serializer.save()
        return Response({
            'order_id': order.id,
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

    # If data is invalid, return a 400 response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
