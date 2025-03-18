import json
import logging
from typing import Any, Dict, List, Set

from api.dto import OrderData, ProductData, ProductDeleteData, Status
from api.models import Order, OrderItem, Product
from api.utils import validate_token
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pydantic import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


logger = logging.getLogger(__name__)

@api_view(['POST'])
@validate_token
def import_order(request: HttpRequest) -> JsonResponse:
    # Add your code here
    """
    Import an order and create associated order items.

    This endpoint processes an incoming request to import an order, including:
    - Validating the provided order request data.
    - Checking if the order already exists.
    - Verifying the existence of all products in the order.
    - Ensuring there is sufficient stock for the products.
    - Creating the order and associated order items if validation passes.

    Arguments:
        request: The HTTP request containing order data in the body.
            {
                "order_number": "ORD-123",
                "total_price": 199.99,
                "customer_name": "John Doe",
                "products": [
                    {
                        "product_number": "PROD-001",
                        "quantity": 2
                    },
                    ...
                ]
            }

    Returns:
        JsonResponse: A response indicating success or failure.
            - 200 OK: Order created successfully.
            - 400 Bad Request: Invalid data or duplicate order number.
            - 404 Not Found: One or more products don't exist.
            - 500 Internal Server Error: Unexpected server error.
    """

    logger.info(f"Received import order request: {request.data}")

    try:
        data: OrderData = OrderData.model_validate(request.data)
    except ValidationError as e:
        logger.error(f"Invalid request data: {e}")
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    if Order.objects.filter(order_number=data.order_number).exists():
        logger.warning(f"Order {data.order_number} already exists")
        return JsonResponse(
            data={"message": f"Order {data.order_number} already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    product_numbers: List[str] = [p.product_number for p in data.products]
    product_dict: Dict[str, Product] = {p.product_number: p for p in Product.objects.filter(product_number__in=product_numbers)}

    missing_products: Set[str] = set(product_numbers) - set(product_dict.keys())
    if missing_products:
        logger.warning(f"Missing products: {missing_products}")
        return JsonResponse(
            data={"message": "Products do not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    insufficient_products: List[str] = [
        p.product_number for p in data.products
        if p.quantity > product_dict[p.product_number].stock_quantity
    ]
    if insufficient_products:
        logger.warning(f"Insufficient stock for products: {insufficient_products}")

    order_status: str = Status.PENDING if insufficient_products else Status.PROCESSING

    try:
        order: Order = Order(
            order_number=data.order_number,
            total_price=data.total_price,
            customer_name=data.customer_name,
            status=order_status
        )
        order.save()
        logger.info(f"Order {order.order_number} imported with ID {order.id}")

        for ordered_product in data.products:
            product: Product = product_dict.get(ordered_product.product_number)

            orderitem: OrderItem = OrderItem(
                order=order,
                product=product,
                quantity=ordered_product.quantity
            )
            orderitem.save()
            logger.info(f"Created ordered item for product {ordered_product.product_number}")
    except Exception as e:
        logger.error(f"Failed to import order for order {data.order_number}: {e}")
        return JsonResponse(
            {"message": "Failed to import order"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        data={"message": "Order imported successfully", "order_id": order.id},
        status=status.HTTP_200_OK,
    )


@api_view(['POST'])
@validate_token
def create_or_update_product(request: HttpRequest) -> JsonResponse:
    """
    Create a new product or update an existing one.

    This endpoint handles both creating a new product or updating an existing product:
    - Validates the request data.
    - If the product with the specified product_number exists, it updates the product's details.
    - The order status of affected orders is also updated based on product availability in stock.
      Orders that are not fully available are marked as 'PENDING', otherwise, they are marked as 'PROCESSING'.
    - If the product does not exist, a new product is created.

    Arguments:
        request: The HTTP request containing product data in the body.
            {
                "product_number": "PROD-001",
                "product_name": "Sample Product",
                "price": 49.99,
                "stock_quantity": 100,
                "description": "Product description"
            }

    Returns:
        JsonResponse: A response indicating or failure.
            - 200 OK: Product created or updated successfully.
            - 400 Bad Request: Invalid data format.
            - 500 Internal Server Error: Unexpected server error.
    """

    logger.info(f"Received create/update product request: {request.data}")

    try:
        data: ProductData = ProductData.model_validate(request.data)
    except ValidationError as e:
        logger.error(f"Invalid request data: {e}")
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    product: Product | None = Product.objects.filter(product_number=data.product_number).first()

    if product:
        try:
            logger.info(f"Updating existing product: {product.product_number}")

            product.product_name = data.product_name
            product.price = data.price
            product.stock_quantity = data.stock_quantity
            product.description = data.description
            product.save()

            affected_orders = Order.objects.filter(ordered_items__product=product).distinct()

            for order in affected_orders:
                if order.status in (Status.DELIVERED, Status.CANCELLED):
                    continue

                all_items_available: bool = all(
                    item.quantity <= item.product.stock_quantity
                    for item in order.ordered_items.all()
                )

                order.status = Status.PROCESSING if all_items_available else Status.PENDING
                order.save()
                logger.debug(f"Updated order {order.order_number} status to {order.status}")
        except Exception as e:
            logger.error(f"Failed to update product {product.product_number}: {e}")
            return JsonResponse(
                {"message": "Failed to update product"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return JsonResponse(
            {"message": "Product updated successfully", "product_id": product.id},
            status=status.HTTP_200_OK
        )
    else:
        try:
            logger.info(f"Creating new product: {data.product_number}")

            product = Product(
                product_number=data.product_number,
                product_name=data.product_name,
                price=data.price,
                stock_quantity=data.stock_quantity,
                description=data.description
            )
            product.save()
            logger.info(f"Created product {product.product_number} successfully")
        except Exception as e:
            logger.error(f"Failed to create product {data.product_number}: {e}")
            return JsonResponse(
                {"message": "Failed to create product"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return JsonResponse(
            {"message": "Product created successfully", "product_id": product.id},
            status=status.HTTP_200_OK
        )


@api_view(['DELETE'])
@validate_token
def delete_product(request: HttpRequest) -> JsonResponse:
    """
    Delete a product and cancel related orders.

    This endpoint deletes a product identified by `product_number`. Before deletion:
    - Validates the request data.
    - It retrieves all orders associated with the product and updates the status of related orders to 'CANCELLED'.
    - Deletes the product from the database.

    Arguments:
        request: The HTTP request containing the product_number in the body.
            {
                "product_number": "PROD-001"
            }

    Returns:
        JsonResponse: A response indicating success or failure
            - 200 OK: Product deleted successfully.
            - 400 Bad Request: Invalid data format.
            - 404 Not Found: Product not found.
            - 500 Internal Server Error: Unexpected server error.
    """

    logger.info(f"Received delete product request: {request.data}")

    try:
        data: ProductDeleteData = ProductDeleteData.model_validate(request.data)
    except ValidationError as e:
        logger.error(f"Invalid request data: {e}")
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    product: Product | None = Product.objects.filter(product_number=data.product_number).first()
    if not product:
        logger.warning(f"Product {data.product_number} not found for deletion")
        return JsonResponse(
            data={"message": f"Product {data.product_number} not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        related_order_items = OrderItem.objects.filter(product=product)
        related_orders = Order.objects.filter(ordered_items__in=related_order_items).distinct()
        related_orders.update(status=Status.CANCELLED)

        logger.info(f"Cancelled orders related to product {data.product_number}")

        product.delete()
        logger.info(f"Product {data.product_number} successfully deleted")
    except Exception as e:
        logger.error(f"Failed to delete product {data.product_number}: {e}")
        return JsonResponse(
            {"message": "Failed to delete product"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return JsonResponse(
        {'message': 'Product deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@validate_token
def get_order_details(request, order_number: str) -> JsonResponse:
    """
    Retrieve detailed information for a specific order.

    This endpoint fetches the details of a specific order based on the provided `order_number`.
    If the order does not exist, it returns a 404 error.

    URL Path Parameter:
        order_number (str): The unique identifier of the order.

    Returns:
        JsonResponse:
            - 200 OK: Get order details successfully.
                - order_number
                - total_price
                - customer_name
                - status
                - updated_time
                - items: A list of items in the order, each containing:
                    * product_number
                    * product_name
                    * quantity
            - 404 Not Found: If the order does not exist, returns an error message.
    """

    logger.info(f"Received get order details request for order: {order_number}")

    try:
        order: Order = Order.objects.get(order_number=order_number)
    except Order.DoesNotExist:
        logger.warning(f"Order {order_number} does not exist")
        return JsonResponse(
            data={"message": f"Order {order_number} does not exist"},
            status=status.HTTP_404_NOT_FOUND
        )

    items: List[Dict[str, Any]] = []
    for item in order.ordered_items.all():
        items.append({
            "product_number": item.product.product_number,
            "product_name": item.product.product_name,
            "quantity": item.quantity
        })

    order_data: Dict[str, Any] = {
        "order_number": order.order_number,
        "total_price": float(order.total_price),
        "customer_name": order.customer_name,
        "status": order.status,
        "updated_time": order.updated_time,
        "items": items
    }

    logger.info(f"Order {order_number} details retrieved successfully")

    return JsonResponse(order_data, status=status.HTTP_200_OK)
