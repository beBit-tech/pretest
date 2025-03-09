from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import Order
from django.core.exceptions import ValidationError

ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    token = request.data.get('token')
    if token != ACCEPTED_TOKEN:
        return HttpResponseBadRequest('Invalid token')

    total_price = request.data.get('total_price')
    product_ids = request.data.get('products')

    if not total_price or not product_ids:
        return HttpResponseBadRequest('Missing fields')

    try:
        order = Order.create_order(total_price=total_price, product_ids=product_ids)
        if order.products.count() != len(product_ids):
            return HttpResponseBadRequest('Invalid product IDs')

        order.save()
        return JsonResponse({'message': 'Order created successfully', 'order_number': order.order_number}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return HttpResponseBadRequest(str(e))