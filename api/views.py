from functools import wraps
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse
from rest_framework.decorators import api_view
from .models import Order
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


@api_view(['POST'])
@check_token
def import_order(request):
    data = json.loads(request.body)
    Order.objects.create(
        order_number=data['order_number'],
        total_price=data['total_price'],
        created_time=data['created_time'],
    )

    return HttpResponse(status=200)


def home(request):
    return HttpResponse("Welcome to my Django app!")