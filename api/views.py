from typing import Any

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import OrderItem, Product
from .serializers import OrderSerializer, ProductSerializer
from .tokens import validate_token

# Create your views here.


ACCEPTED_TOKEN = "omni_pretest_token"


@api_view(["GET", "POST"])
def product_list_create(request: Request) -> Response:
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"products": serializer.data})
    elif request.method == "POST":
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"product": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response(
        {"error": "invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["GET", "PUT", "DELETE"])
def product_retrieve_update_delete(request: Request, pk: int) -> Response:
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(
            {"error": f"Product with ID {pk} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response({"product": serializer.data})
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"product": serializer.data}, status=status.HTTP_200_OK)
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(
        {"error": "invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )


@api_view(["POST"])
@validate_token
@transaction.atomic
def import_order(request: Request) -> Response:
    data = request.data
    items: list[dict[str, Any]] = data.get("items", [])
    if not items:
        return Response(
            {"error": "Empty item list"}, status=status.HTTP_400_BAD_REQUEST
        )

    total_price = 0
    order_items = []

    try:
        for item in items:
            product = Product.objects.get(pk=item.get("id"))
            total_price += product.price * item.get("quantity")
            order_items.append(
                {
                    "product": product,
                    "quantity": item.get("quantity"),
                    "unit_price": product.price,
                }
            )
    except Product.DoesNotExist:
        return Response(
            {"error": f"Product with ID {item.get('id')} not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = OrderSerializer(
        data={"order_number": data.get("order_number"), "total_price": total_price}
    )
    if serializer.is_valid():
        order = serializer.save()
        for order_item in order_items:
            OrderItem.objects.create(
                order=order,
                product=order_item.get("product"),
                quantity=order_item.get("quantity"),
                unit_price=order_item.get("unit_price"),
            )
        return Response({"order": serializer.data}, status=status.HTTP_201_CREATED)

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
