from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from api.models import Order
from .serializers import OrderSerializers
from django.utils.timezone import now


# Token used to authorize API requests
ACCEPTED_TOKEN = ('omni_pretest_token')


# @api_view(['POST'])
# def import_order(request):
#     token = request.data.get('token')
#     if token != ACCEPTED_TOKEN:
#         return Response({'error': 'Un authorized'}, status=status.HTTP_401_UNAUTHORIZED)

#     order_number = request.data.get('order_number')
#     total_price = request.data.get('total_price')

#     if not order_number or not total_price:
#         return Response({'error': 'Missing data'}, status=status.HTTP_400_BAD_REQUEST)

#     try:
#         order = Order(order_number=order_number, total_price=total_price)
#         order.save()
#         return Response({'message': 'Order imported successfully'}, status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def import_order(request):
    """
    API to import an order using POST request.
    Validates the provided token and order data, then creates a new order.
    """
    token = request.data.get('token')
    if token != ACCEPTED_TOKEN:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    # Deserialize and validate input data
    serializer = OrderSerializers(data=request.data)  # OrderSerializers validates and prepares Order model data
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Order imported successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# API to return a list of all orders
@api_view(['GET'])
def orderList(request):
    """
    API to return a list of all orders.
    """
    order = Order.objects.all()
    serializer = OrderSerializers(order, many=True)  # Serializes multiple Order instances
    return Response(serializer.data)

# API to return the details of a single order
@api_view(['GET'])
def orderDetail(request, pk):
    """
    API to return the details of a single order.
    """
    order = Order.objects.get(id=pk)
    serializer = OrderSerializers(order, many=False)  # Serializes a single Order instance
    return Response(serializer.data)

# API to update an existing order
@api_view(['POST'])
def orderUpdate(request, pk):
    """
    API to update an existing order.
    Validates the provided token and updates the specified order.
    """
    token = request.data.get('token')
    if token != ACCEPTED_TOKEN:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    order = Order.objects.get(id=pk)

    # Deserialize and validate updated data
    serializer = OrderSerializers(instance=order, data=request.data)  # OrderSerializers updates the Order instance
    if serializer.is_valid():
        order.created_time = now()
        order.save()
        serializer.save()

    return Response(serializer.data)

# API to delete an existing order
@api_view(['DELETE'])
def orderDelete(request, pk):
    """
    API to delete an existing order.
    Validates the provided token and deletes the specified order if it exists.
    """
    token = request.data.get('token')
    if token != ACCEPTED_TOKEN:
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        order = Order.objects.get(id=pk)
        order.delete()
        return Response({'message': 'Delete success'}, status=status.HTTP_200_OK)
    except Order.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)