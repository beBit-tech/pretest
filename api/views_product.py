# api/views_product.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Product
from .auth_utils import validate_access_token


@api_view(["POST"])
@validate_access_token
def create_product(request, data):
    """
    建立新產品的 API
    """
    product_id = data.get("product_id")
    name = data.get("name")
    price = data.get("price")
    description = data.get("description", "")

    if not product_id or not name or not price:
        return Response({"error": "Missing required fields"}, status=400)

    # 建立並儲存商品
    product = Product.objects.create(
        product_id=product_id,
        name=name,
        price=price,
        description=description
    )

    return Response({
        "message": "Product created successfully",
        "product_id": product.product_id
    }, status=201)

@api_view(["DELETE"])
@validate_access_token
def delete_product(request, data):
    """
    刪除指定 product_id 的商品。
    """
    product_id = data.get("product_id")
    if not product_id:
        return Response({"error": "Missing product_id"}, status=400)

    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return Response({"error": f"Product {product_id} does not exist."}, status=404)

    product.delete()
    return Response({"message": f"Product {product_id} deleted successfully"}, status=200)