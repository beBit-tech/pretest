from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .AccessValidation import validate_token

#old validation logic
'''
def validate_token(token):
    return token == ACCEPTED_TOKEN
'''


@api_view(['POST'])
@validate_token  # decorator
def import_order(request):
    serializer = OrderSerializer(data=request.data)

    # Data Validation
    if serializer.is_valid():
        order = serializer.save()
        return Response({
            'order_id': order.id,
            'order': OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)

    # Data invalid = 400 response 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
