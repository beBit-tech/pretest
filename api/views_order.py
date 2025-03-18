# api/views_order.py

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, Product, OrderProduct
from .utils import generate_order_number
from .auth_utils import validate_access_token


@api_view(["POST"])
@validate_access_token
def import_order(request, data):
    """
    接收 JSON 格式的訂單資訊，並自動計算 total_price、建立 Order 與 OrderProduct。
    """
    products = data.get("products")
    if not products:
        return Response({"error": "No products provided"}, status=400)

    # 1. 產生唯一的訂單編號
    order_number = generate_order_number()

    # 2. 建立一筆 Order，先讓 total_price = 0
    order = Order.objects.create(order_number=order_number, total_price=0)

    total_price_acc = 0

    # 3. 處理 products
    for item in products:
        product_id = item.get("product_id")
        quantity = item.get("quantity")

        # 檢查必要欄位
        if not product_id or not quantity:
            order.delete()
            return Response(
                {"error": "Each product must contain product_id and quantity."},
                status=400
            )

        # 查詢 Product
        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            order.delete()
            return Response(
                {"error": f"Product {product_id} does not exist."},
                status=400
            )
        
        # 確認庫存是否足夠
        if quantity > product.stock:
            order.delete()
            return Response(
                {"error": f"Insufficient stock for product {product_id}"},
                status=400
            )

        # 計算該商品總額 (price * quantity)
        sub_total = product.price * quantity
        total_price_acc += sub_total

        # 扣掉庫存
        product.stock -= quantity
        product.save()

        # 建立對應的 OrderProduct
        OrderProduct.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price_at_order_time=product.price
        )

    # 4. 更新訂單金額
    order.total_price = total_price_acc
    order.save()

    # 5. 回傳成功
    return Response({
        "message": "Order created successfully",
        "order_number": order.order_number,
        "total_price": float(order.total_price)
    }, status=201)


@api_view(["GET"])
def order_detail(request, order_number):
    """
    查詢訂單明細的 API
    """
    try:
        order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=404)

    order_products = OrderProduct.objects.filter(order=order)
    product_list = [
        {
            "product_name": op.product.name,
            "quantity": op.quantity,
            "price_at_order_time": float(op.price_at_order_time)
        }
        for op in order_products
    ]

    return Response({
        "order_number": order.order_number,
        "total_price": float(order.total_price),
        "created_time": order.created_time,
        "products": product_list
    })
