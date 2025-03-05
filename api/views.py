from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product
from .serializers import OrderSerializer, ProductSerializer
from .tokens import validate_token

# Create your views here.


ACCEPTED_TOKEN = "omni_pretest_token"


@api_view(["POST"])
@validate_token
def import_order(request: Request) -> Response:
    data = request.data

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"order": serializer.data}, status=status.HTTP_201_CREATED)

    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def product_list_create(request: Request) -> Response:
    if request.method == "GET":
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response({"product": serializer.data})
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
            return Response(
                {"product": serializer.data}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    elif request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(
        {"error": "invalid method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
    )
