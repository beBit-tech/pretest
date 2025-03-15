import json
from functools import wraps

from api.models import Order
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from pydantic import BaseModel, ValidationError
from rest_framework.decorators import api_view

# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


class OrderData(BaseModel):
    order_number: str
    total_price: float


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
        data = OrderData.model_validate(request.data.dict())
    except ValidationError as e:
        return HttpResponseBadRequest(f"Invalid request data: {e}")

    order = Order(
        order_number=data.order_number,
        total_price=data.total_price
    )
    order.save()

    return JsonResponse(
        data={"message": "Order imported successfully", "order_id": order.id},
        status=200,
    )
