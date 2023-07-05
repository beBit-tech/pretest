from functools import wraps
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Order, OrderProduct, Product
from api.serializers import ProductSerializer
import json
# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')

def check_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token != ACCEPTED_TOKEN:
            return HttpResponseBadRequest()
        return view_func(request, *args, **kwargs)
    return _wrapped_view

class CustomException(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def __str__(self):
        return f'{self.message} (status code: {self.status_code})'


@api_view(['POST'])
@check_token
def import_order(request):
    import_data = json.loads(request.body)

    with transaction.atomic():
        try:
            import_products = import_data['products']
            import_product_ids = [p['product_number'] for p in import_products]
            cur_products = Product.objects.in_bulk(import_product_ids)

            # Check all products in import order exist
            cur_and_import_products = list()
            for import_product in import_products:
                import_product_number = import_product['product_number']
                cur_product = cur_products.get(import_product_number)
                if not cur_product:
                    error_message = f"Product [{import_product_number}] does not exist."
                    raise CustomException(error_message, 400)
                cur_and_import_products.append([cur_product, import_product])

            # Check if product quantity is sufficient
            for cur_product, import_product in cur_and_import_products:
                import_order_quantity = import_product['quantity']
                if cur_product.amount < import_order_quantity:
                    error_message = (
                        f"Not enough quantity for product [{cur_product.product_number}]. "
                        f"Required: {import_order_quantity}, Available: {cur_product.amount}"
                    )
                    raise CustomException(error_message, 400)

            # Create order object
            order_total_price = 0
            for cur_product, import_product in cur_and_import_products:
                order_total_price += import_product['quantity'] * cur_product.price
            order = Order.objects.create(
                order_number=import_data['order_number'],
                total_price=order_total_price,
                payment_method=import_data['payment_method'],
            )

            # Bulk create OrderProduct objects
            order_products_to_create = [
                OrderProduct(
                    product=cur_product,
                    order=order,
                    quantity=import_product['quantity'],
                )
                for cur_product, import_product in cur_and_import_products
            ]
            OrderProduct.objects.bulk_create(order_products_to_create)

             # Bulk update Product objects
            for cur_product, import_product in cur_and_import_products:
                cur_product.amount -= import_product['quantity']
                if cur_product.amount == 0:
                    cur_product.status = 'out_of_stock'
            Product.objects.bulk_update(
                [product[0] for product in cur_and_import_products],
                ['amount', 'status'],
            )

        except CustomException as e:
            transaction.set_rollback(True)
            return Response({'error': e.message}, status=e.status_code)
        except Exception as e:
            transaction.set_rollback(True)
            return Response({'error': str(e)}, status=500)

    return HttpResponse(status=200)

@api_view(['POST'])
def create_product(request):
    product_data = request.data

    if isinstance(product_data, list):
        serializer = ProductSerializer(data=product_data, many=True)
    else:
        serializer = ProductSerializer(data=product_data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)

    return Response(serializer.errors, status=400)


@api_view(['DELETE'])
def delete_products(request):
    product_numbers = request.data.get('product_numbers')

    deleted_numbers = list()
    not_found_numbers = list()

    for product_number in product_numbers:
        try:
            product = Product.objects.get(pk=product_number)
            product.delete()
            deleted_numbers.append(product_number)
        except Product.DoesNotExist:
            not_found_numbers.append(product_number)

    response_data = {
        'deleted_products': deleted_numbers,
        'not_found_products': not_found_numbers,
    }

    return Response(response_data, status=200)


@api_view(['PUT', 'PATCH'])
def update_products(request):
    product_data = request.data

    updated_numbers = list()
    not_found_numbers = list()

    for data in product_data:
        product_number = data.get('product_number')
        try:
            product = Product.objects.get(pk=product_number)
            serializer = ProductSerializer(product, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated_numbers.append(product_number)
            else:
                not_found_numbers.append(product_number)
        except Product.DoesNotExist:
            not_found_numbers.append(product_number)

    response_data = {
        'updated_products': updated_numbers,
        'not_found_products': not_found_numbers,
    }

    return Response(response_data)


def home(request):
    return HttpResponse("Welcome to my Django app!")