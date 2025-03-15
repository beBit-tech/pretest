import json
from functools import wraps
from typing import List, Optional

from api.models import Order, OrderItem, Product
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pydantic import BaseModel, Field, ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


class OrderItemData(BaseModel):
    product_number: str
    quantity: int


class OrderData(BaseModel):
    order_number: str
    total_price: float
    customer_name: str
    products: List[OrderItemData] = Field(min_items=1)


class ProductData(BaseModel):
    product_number: str
    product_name: str
    price: float
    stock_quantity: int
    description: Optional[str] = ""


class ProductDeleteData(BaseModel):
    product_number: str


def validate_token(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {ACCEPTED_TOKEN}":
            return HttpResponseBadRequest("Invalid token")
        return func(request, *args, **kwargs)
    return wrapper


@api_view(['POST'])
@validate_token
def import_order(request):
    # Add your code here
    try:
        data = OrderData.model_validate(request.data)
    except ValidationError as e:
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    order = Order(
        order_number=data.order_number,
        total_price=data.total_price,
        customer_name=data.customer_name
    )
    order.save()

    product_numbers = [p.product_number for p in data.products]
    products_dict = {p.product_number: p for p in Product.objects.filter(product_number__in=product_numbers)}

    for ordered_product in data.products:
        product = products_dict.get(ordered_product.product_number)
        if not product:
            return JsonResponse(
                data={"message": f"Product {ordered_product.product_number} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )

        orderitem = OrderItem(
            order=order,
            product=product,
            quantity=ordered_product.quantity
        )
        orderitem.save()

    return JsonResponse(
        data={"message": "Order imported successfully", "order_id": order.id},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@validate_token
def create_or_update_product(request):
    try:
        data = ProductData.model_validate(request.data)
    except ValidationError as e:
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    product = Product.objects.filter(product_number=data.product_number).first()

    if product:
        product.product_name = data.product_name
        product.price = data.price
        product.stock_quantity = data.stock_quantity
        product.description = data.description
        product.save()

        return JsonResponse(
            {"message": "Product updated successfully", "product_id": product.id},
            status=status.HTTP_200_OK
        )
    else:
        product = Product(
            product_number=data.product_number,
            product_name=data.product_name,
            price=data.price,
            stock_quantity=data.stock_quantity,
            description=data.description
        )
        product.save()

        return JsonResponse(
            {"message": "Product created successfully", "product_id": product.id},
            status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@validate_token
def delete_product(request):
    try:
        data = ProductDeleteData.model_validate(request.data)
    except ValidationError as e:
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    product = Product.objects.filter(product_number=data.product_number).first()
    if not product:
        return JsonResponse(
            data={"message": f"Product {data.product_number} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    product.delete()

    return JsonResponse(
        {'message': 'Product deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@validate_token
def get_order_details(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return JsonResponse(
            data={"message": f"Order {order_number} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    items = []
    for item in order.ordered_items.all():
        items.append({
            "product_number": item.product.product_number,
            "product_name": item.product.product_name,
            "quantity": item.quantity
        })

    order_data = {
        "order_number": order.order_number,
        "total_price": float(order.total_price),
        "customer_name": order.customer_name,
        "status": order.status,
        "created_time": order.created_time,
        "items": items
    }

    return JsonResponse(order_data, status=status.HTTP_200_OK)
