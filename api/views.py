from django.http import HttpResponseBadRequest, JsonResponse
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Order
from .decorators import check_access_token

ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
@check_access_token
def import_order(request):
    total_price = request.data.get('total_price')
    product_ids = request.data.get('product_ids')

    if not total_price or not product_ids:
        return HttpResponseBadRequest('Missing fields')

    try:
        order = Order.create_order(total_price=total_price, product_ids=product_ids)
        return JsonResponse({'message': 'Order created successfully', 'order_number': order.order_number}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return HttpResponseBadRequest(str(e))