from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.adapter.repository.order.order_repository import OrderRepository
from api.adapter.repository.product.product_repository import ProductRepository
from api.adapter.controller.decoractor import token_required
from api.adapter.controller.order.order_serializer import OrderSerializer
from api.use_case.order.import_order.import_order import ImportOrder
from api.use_case.order.import_order.import_order_input import ImportOrderInput
from api.use_case.order.import_order.import_order_output import ImportOrderOutput
from api.use_case.order.get_all_orders.get_all_orders import GetAllOrders
from api.use_case.order.get_all_orders.get_all_orders_output import GetAllOrdersOutput

@token_required
@api_view(['POST'])
def import_order(request):
    serializer = OrderSerializer(data = request.data)
    if serializer.is_valid():
        validated_data = serializer.validated_data

        total_price = validated_data["total_price"]
        created_time = validated_data["created_time"]
        order_lines = validated_data["order_lines"]
        
        input = ImportOrderInput(total_price = total_price, created_time=created_time, order_lines = order_lines)
        order_repo = OrderRepository()
        product_repo = ProductRepository()
        output: ImportOrderOutput = ImportOrder(order_repo = order_repo, product_repo = product_repo).execute(input = input)
        
        if output.result:
            return Response({
                "number": output.number,
                "message": "Order created successfully."
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "error": str(output.exception),
                "message": "Order creation failed."
            }, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@token_required
@api_view(['GET'])
def get_all_orders(request):
    repo = OrderRepository()
    output: GetAllOrdersOutput = GetAllOrders(repo).execute()
    
    if output.result:
        return Response({
            'orders': output.orders,
            'message': 'Fetch orders successfully.'
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'error': str(output.exception),
            'message': 'Fetch orders failed.'
        }, status=status.HTTP_400_BAD_REQUEST)