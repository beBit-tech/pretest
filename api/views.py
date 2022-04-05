from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .authentications import CustomAuthentication



from .models import Product, Order
from .serializers import OrderSerializer


# ACCEPTED_TOKEN = ('omni_pretest_token') <-- moved to authentications.py

@api_view(['GET'])
def api_root(request):
    return Response({
        'orders': reverse('import-order', request=request)
    })


@api_view(['GET', 'POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def import_order(request):
    if request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# http POST http://localhost:8008/api/import-order/ "Authorization: Token omni_pretest_token"
