from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from api.models import Order,Product,Customer,OrderProduct
from django.utils.dateparse import parse_datetime
import logging
from datetime import datetime
from .decorators import token_required
from .constants import ERROR_CODES

logger = logging.getLogger(__name__)

# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
@token_required
def import_order(request):
    """
    Add new order to database
    ================================================
    Steps:
    1. Validate, check if token is in ACCEPTED_TOKEN
    2. Parse data from request payload
    3. Add new order object into postgres db
    4. Add Object Product pair and calculate total_price

    Input:
    token: str (required)
    customer_uid : str (required)
    products: [{uid, count}] (required)
    """
    try:
        data = json.loads(request.body)

        # get order info from json
        customer_uid = data.get("customer_uid",'')
        products = data.get("products",[])

        # check required data
        if not customer_uid:
            return Response({"message": "customer_uid is required",'error_code':ERROR_CODES['CUSTOMER_UID_EMPTY']}, status=400)
        if not products:
            return Response({"message": "Product is empty",'error_code':ERROR_CODES['PRODUCT_EMPTY']}, status=400)

        exist_customer = Customer.objects.filter(uid=customer_uid).first()
        if not exist_customer:
            return Response({"message": "customer not exist",'error_code':ERROR_CODES['CUSTOMER_NOT_EXIST']}, status=400)

        # Calculate total price
        total_price = 0
        for item in products:
            product_uid = item.get('uid')
            count = item.get('count', 1)
            if count < 0:
                return Response({"message": "Product count less than 0",'error_code':ERROR_CODES['INVALID_PRODUCT_COUNT']}, status=400)
            try:
                product = Product.objects.get(uid=product_uid)
            except Product.DoesNotExist:
                return Response({'message': f'Product with UID {product_uid} not found','error_code':ERROR_CODES['PRODUCT_NOT_EXIST']}, status=400)
            total_price += product.price * count

        # add new order to db
        new_order = Order.objects.create(
            customer=exist_customer,
            total_price=total_price
        )

        # Add Object Product pair
        for item in products:
            product_uid = item.get('uid')
            count = item.get('count', 1)
            product = Product.objects.get(uid=product_uid)
            OrderProduct.objects.create(
                order=new_order,
                product=product,
                count=count
            )

        return Response({"message": f"New order added, order number: {new_order.order_number}"}, status=200)
    except json.JSONDecodeError:
        return Response({"message": "Invalid JSON format",'error_code':ERROR_CODES['INVALID_JSON_FORMAT']}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@token_required
def add_product(request):
    """
    Add new product to database

    Input:
    token: str (required)
    name: str (required)
    price : int (required)
    """
    try:
        data = json.loads(request.body)

        # get order info from json
        name = data.get("name",'')
        price = data.get("price",-1)

        # check required data
        if not name:
            return Response({"message": "Name required",'error_code':ERROR_CODES['PRODUCT_NAME_EMPTY']}, status=400)
        if price<0:
            return Response({"message": "Price empty or less than 0",'error_code':ERROR_CODES['INVALID_PRODUCT_PRICE']}, status=400)

        # add new order to db
        new_product = Product.objects.create(
            name=name,
            price=price
        )
        return Response({"message": "New product added"}, status=200)
    except json.JSONDecodeError:
        return Response({"message": "Invalid JSON format",'error_code':ERROR_CODES['INVALID_JSON_FORMAT']}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['POST'])
@token_required
def add_customer(request):
    """
    Add new customer to database

    Input:
    token: str (required)
    name: str (required)
    """
    try:
        data = json.loads(request.body)

        # get order info from json
        name = data.get("name",'')

        # check required data
        if not name:
            return Response({"message": "Name required",'error_code':ERROR_CODES['CUSTOMER_NAME_EMPTY']}, status=400)

        # add new order to db
        new_customer = Customer.objects.create(
            name=name
        )
        return Response({"message": "New customer added"}, status=200)
    except json.JSONDecodeError:
        return Response({"message": "Invalid JSON format",'error_code':ERROR_CODES['INVALID_JSON_FORMAT']}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

@api_view(['GET'])
def get_order_detail(request, order_number):
    '''
    Show detail of a order

    Input:
    order_number: str

    Output:
    order_number,
    customer,
    total_price,
    products,
    created_time
    '''
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Order not found', 'error_code': ERROR_CODES['ORDER_NOT_EXIST']},
            status=400
        )

    products = OrderProduct.objects.filter(order=order).select_related('product')
    product_list = [
        {
            'product_uid': op.product.uid,
            'product_name': op.product.name,
            'count': op.count,
            'price': float(op.product.price)
        } for op in products
    ]

    data = {
        'order_number': order.order_number,
        'customer': order.customer.uid,
        'total_price': float(order.total_price),
        'products': product_list,
        'created_time': order.created_time.isoformat()
    }
    return Response(data)

@api_view(['GET'])
def get_customer_orders(request, customer_uid):
    '''
    Return detail of all orders by a customer

    Input:
    customer_uid: str

    Output:
    customer_uid
    customer_name
    orders
    '''
    try:
        customer = Customer.objects.get(uid=customer_uid)
    except Customer.DoesNotExist:
        return Response(
            {'message': 'Customer not found', 'error_code': ERROR_CODES['CUSTOMER_NOT_EXIST']},
            status=400
        )

    orders = Order.objects.filter(customer=customer).order_by('-created_time')
    order_list = []

    for order in orders:
        products = OrderProduct.objects.filter(order=order).select_related('product')
        product_list = [
            {
                'product_uid': op.product.uid,
                'product_name': op.product.name,
                'count': op.count,
                'price': float(op.product.price)
            }
            for op in products
        ]

        order_list.append({
            'order_number': order.order_number,
            'total_price': float(order.total_price),
            'products': product_list,
            'created_time': order.created_time.isoformat()
        })

    return Response({
        'customer_uid': customer.uid,
        'customer_name': customer.name,
        'orders': order_list
    })

@api_view(['POST'])
@token_required
def delete_orders(request):
    order_numbers = request.data.get('order_numbers')

    # Check invalid order_number
    if not order_numbers or not isinstance(order_numbers, list):
        return Response({
            "message": "Missing or invalid order_numbers list",
            'error_code': ERROR_CODES['INVALID_ORDER']
        }, status=400)

    # Check existing Order
    existing_orders = Order.objects.filter(order_number__in=order_numbers)
    deleted_order_count = len(existing_orders)
    existing_order_numbers = set(existing_orders.values_list('order_number', flat=True))
    not_found = list(set(order_numbers) - existing_order_numbers)

    deleted_count, _ = existing_orders.delete()

    return Response({
        "message": f"Order(s) deleted successfully",
        "success": deleted_order_count,
        "fail": len(not_found),
        "not_found": not_found
    }, status=200)