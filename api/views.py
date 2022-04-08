from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Order,Product,ProductOrder
from .serializers import OrderSerializer,OrderImportSerializer,ProductSerializer,OrderDetailSerializer
from .permissions import AcceptedToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(method='post',operation_summary="Import Order by Product_number", operation_description="Can enter mutiple products in 'products_data', e.g. products_data:[{product1...},{product2...}]",request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'buyer': openapi.Schema(type=openapi.TYPE_STRING, description='Name',example="Alan"),
        'products_data':openapi.Schema(type=openapi.TYPE_ARRAY,description='Can enter mutiple products, seperate by {},',
            items=openapi.Items(type=openapi.TYPE_OBJECT,
            properties={
                'product_number':openapi.Schema(type=openapi.FORMAT_UUID,example="5c04b6d8-0003-4d10-bb0c-6d9e9ec43653"),
                'quantity':openapi.Schema(type=openapi.TYPE_INTEGER,example=2)
            })
        )
    }
))

@api_view(['POST'])
@AcceptedToken
def import_order(request):
    '''Create a new order'''
    serializer = OrderImportSerializer(data=request.data)
    if serializer.is_valid():
        order=serializer.save()    
        return Response(order,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

#Get all orders

@api_view(['GET'])
def orders_list(request):
    '''List all orders'''
    orders = Order.objects.all()
    serializer = OrderSerializer(orders,many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='put', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'buyer': openapi.Schema(type=openapi.TYPE_STRING, description='Name',example="Alan"),
        'products_data':openapi.Schema(type=openapi.TYPE_ARRAY,description='Can enter mutiple products, seperate by {},',items=openapi.Items(type=openapi.TYPE_OBJECT,properties={
            'product_number':openapi.Schema(type=openapi.FORMAT_UUID,example="5c04b6d8-0003-4d10-bb0c-6d9e9ec43653"),
            'quantity':openapi.Schema(type=openapi.TYPE_INTEGER,example=2)
        }))
    }
))
@api_view(['GET','PUT','DELETE'])
@AcceptedToken
def orders_detail(request,pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        detail_order = order.orders.all()
        order_serializer = OrderSerializer(order)
        detail_serializer = OrderDetailSerializer(detail_order,many=True)
        res={
            'Order Summary':order_serializer.data,
            'ALL Products':detail_serializer.data
        }
        return Response(res)

    elif request.method == 'PUT':
        serializer = OrderImportSerializer(order,data=request.data)
        if serializer.is_valid():
            order=serializer.save()
            return Response(order,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        productorders = order.orders.all()
        for productorder in productorders:
            product=productorder.product
            product.quantity += productorder.quantity
            product.save()    
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


#Product
@swagger_auto_schema(method='post',operation_description="status will be true in default.(which means it is available)", request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING,example="TV"),
        'price': openapi.Schema(type=openapi.FORMAT_DECIMAL, description='Decimal(12,2)',example=36680),
        'quantity':openapi.Schema(type=openapi.TYPE_INTEGER,example="100"),
        'status':openapi.Schema(type=openapi.TYPE_BOOLEAN,example=True),
    }
))
@api_view(['POST'])
@AcceptedToken
def import_product(request):
    '''create a new product'''
    #pass context and validate it in serializer
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)  

#Get all orders
@api_view(['GET'])
def products_list(request):
    '''List all products'''
    products = Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='put',operation_description="status will be true in default.(which means it is available)", request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'title': openapi.Schema(type=openapi.TYPE_STRING,example="TV"),
        'price': openapi.Schema(type=openapi.FORMAT_DECIMAL, description='Decimal(12,2)',example=36680),
        'quantity':openapi.Schema(type=openapi.TYPE_INTEGER,example="100"),
        'status':openapi.Schema(type=openapi.TYPE_BOOLEAN,example=True),
    }
))
@api_view(['GET','PUT','DELETE'])
@AcceptedToken
def products_detail(request,pk):
    """
    Retrieve, update or delete a product.
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data,status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if ProductOrder.objects.filter(product=product).exists():
            return Response(data="Can't DELETE!. The Product has been order by Others. ",status=status.HTTP_403_FORBIDDEN)  
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)            
