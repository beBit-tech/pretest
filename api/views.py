from functools import wraps

from django.http import HttpResponseBadRequest
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Customer, Order, Product
from .serializers import CustomerSerializer, OrderSerializer, ProductSerializer

# Create your views here.


ACCEPTED_TOKEN = "omni_pretest_token"


def check_token(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token != ACCEPTED_TOKEN:
            return Response(
                {"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return func(request, *args, **kwargs)

    return wrapper


@api_view(["POST"])
@check_token
def import_order(request):
    # Parse the data from request using serializer
    serializer = OrderSerializer(data=request.data)

    # Validate the data
    if serializer.is_valid():
        # save the valid data
        order = serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    # If data is invalid, return a 400 response
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@check_token
def create_customer(request):
    serializer = CustomerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@check_token
def create_product(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@check_token
def get_products(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@check_token
def get_orders_by_customer(request, username):
    customer = Customer.objects.get(username=username)
    try:
        print(customer)
    except Customer.DoesnotExist:
        return Response(
            {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
        )
    orders = Order.objects.filter(customer=customer)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
