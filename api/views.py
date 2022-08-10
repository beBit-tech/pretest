from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from .permission import VerifyToken
# Create your views here.





@api_view(['GET'])
def list_order(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders,many = True)
    return JsonResponse({'orders':serializer.data})


@api_view(['POST'])
@VerifyToken
def import_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response({'error':'unvalid input data'},status=status.HTTP_400_BAD_REQUEST)   

@api_view(['GET','PUT','DELETE'])
def specific_order(request,id):
    try:
        order = Order.objects.get(pk=id)
    except Order.DoesNotExist:
        return Response({'error':'order not found'},status=status.HTTP_404_NOT_FOUND)     
    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)