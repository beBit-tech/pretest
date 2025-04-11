from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from django.utils.timezone import now
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