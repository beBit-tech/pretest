from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import IntegrityError

from .serializers import OrderSerializer, ProductSerializer
from .models import Product, Order
from .util import token_validation
from datetime import timedelta

# Create your views here.

@api_view(["POST"])
@token_validation
def import_order(request: Request):
    """
    Import an order with order items
    Request JSON format:
    {
        "order_items": [
            {
                "product_title": "Product 1",
                "quantity": 2
            },
            {
                "product_title": "Product 2",
                "quantity": 1
            }, 
            ...
        ]
    }
    """
    serializers = OrderSerializer(data=request.data)
    if serializers.is_valid():
        try:
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({"error": "Product with title already exists in the order"}, status=status.HTTP_409_CONFLICT)
    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@token_validation
def list_orders(request):
    """List all orders in descending order of creation time."""
    orders = Order.objects.all().order_by("-created_at")

    paginator = PageNumberPagination()
    result_page = paginator.paginate_queryset(orders, request)

    serializer = OrderSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

@api_view(["GET"])
@token_validation
def get_order_by_number(_: Request, order_number):
    """
    Get order by order number.
    url: /api/get-order-by-number/<uuid:order_number>/
    """
    order = get_object_or_404(Order, order_number=order_number)
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(["GET"])
@token_validation
def get_order_by_product(request:Request, product_number):
    """
    Get all orders in descending order that contain a specific product.
    url: /api/get-order-by-product/<uuid:product_number>/
    """
    product = get_object_or_404(Product, product_number=product_number)

    order_items = product.product_items.all()
    orders = [order_item.order for order_item in order_items]
    orders.sort(key=lambda order: -order.created_at.timestamp())

    paginator = PageNumberPagination()
    paginated_orders = paginator.paginate_queryset(orders, request)

    serializer = OrderSerializer(paginated_orders, many=True)
    return paginator.get_paginated_response(serializer.data)
    
@api_view(["DELETE"])
@token_validation
def delete_order(_: Request, order_number):
    """
    Delete an order by order number(Soft Delete).
    url: /api/delete-order/<uuid:order_number>/
    """
    order = get_object_or_404(Order, order_number=order_number)
    if order.status == "F" or order.status == "C":
        return Response({"error": "Order is already marked as FAILED or COMPLETED."}, status=status.HTTP_400_BAD_REQUEST)
    
    if order.created_at < timezone.now() - timedelta(days=1):
        return Response({"error": "Order cannot be deleted after 1 day."}, status=status.HTTP_400_BAD_REQUEST)

    with transaction.atomic():
        order.status = "F"
        order.save()

    return Response({"message": "Order status updated to FAILED."}, status=status.HTTP_200_OK)
    
@api_view(["POST"])
@token_validation
def create_product(request):
    """Create a new product."""
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
@token_validation
def delete_product(_: Request, product_number):
    """Delete a product by product number."""
    product = get_object_or_404(Product, product_number=product_number)

    with transaction.atomic():
        product.delete()

    return Response({"message": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

@api_view(["PATCH"])
@token_validation
def update_product(request, product_number):
    """Update a product by product number."""
    product = get_object_or_404(Product, product_number=product_number)

    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Product updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)