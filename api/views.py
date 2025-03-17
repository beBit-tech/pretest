import json

from api.dto import OrderData, ProductData, ProductDeleteData, Status
from api.models import Order, OrderItem, Product
from api.utils import validate_token
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pydantic import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['POST'])
@validate_token
def import_order(request):
    # Add your code here
    try:
        data = OrderData.model_validate(request.data)
    except ValidationError as e:
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    if Order.objects.filter(order_number=data.order_number).exists():
        return JsonResponse(
            data={"message": f"Order {data.order_number} already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product_numbers = [p.product_number for p in data.products]
    product_dict = {p.product_number: p for p in Product.objects.filter(product_number__in=product_numbers)}

    missing_products = set(product_numbers) - set(product_dict.keys())
    if missing_products:
        return JsonResponse(
            data={"message": "Products do not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    insufficient_products = [
        p.product_number for p in data.products
        if p.quantity > product_dict[p.product_number].stock_quantity
    ]

    order_status = Status.PENDING if insufficient_products else Status.PROCESSING

    order = Order(
        order_number=data.order_number,
        total_price=data.total_price,
        customer_name=data.customer_name,
        status=order_status
    )
    order.save()

    for ordered_product in data.products:
        product = product_dict.get(ordered_product.product_number)

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

        affected_orders = Order.objects.filter(ordered_items__product=product).distinct()

        for order in affected_orders:
            if order.status in (Status.DELIVERED, Status.CANCELLED):
                continue

            all_items_available = all(
                item.quantity <= item.product.stock_quantity
                for item in order.ordered_items.all()
            )

            order.status = Status.PROCESSING if all_items_available else Status.PENDING
            order.save()

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

    related_order_items = OrderItem.objects.filter(product=product)
    related_orders = Order.objects.filter(ordered_items__in=related_order_items).distinct()
    related_orders.update(status=Status.CANCELLED)

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
        "updated_time": order.updated_time,
        "items": items
    }

    return JsonResponse(order_data, status=status.HTTP_200_OK)
