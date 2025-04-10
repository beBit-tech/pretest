from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from django.utils.timezone import now
from api.models import Order
from django.utils.dateparse import parse_datetime
import logging
from datetime import datetime


logger = logging.getLogger(__name__)

# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    """
    Add new order to database
    ================================================
    Steps:
    1. Validate, check if token is in ACCEPTED_TOKEN
    2. Parse data from request payload
    3. Add new order object into postgres db

    Input:
    token: str (required)
    order_number: str (required)
    total_price : int (required)
    created_time: datetime (optional, default as current time)
    """
    # Add your code here
    try:
        # Validating access token from request data, suppose there is a token in post request payload
        data = json.loads(request.body)
        token = data.get('token','')
        if not token:
            return JsonResponse({"error": "Unauthorized: token required"}, status=401)
        if token not in ACCEPTED_TOKEN:
            return JsonResponse({"error": "Unauthorized: Invalid token"}, status=401)

        # get order info from json
        order_number = data.get("order_number",'')
        total_price = data.get("total_price",'')
        created_time = data.get("created_time",None)

        # check created_time format
        if created_time:
            try:
                created_time = datetime.fromisoformat(created_time.replace("Z", "+00:00"))
            except ValueError:
                return JsonResponse({"error": "Invalid created_time format"}, status=400)
        else:
            created_time = now()

        # check required data
        if not order_number:
            return JsonResponse({"error": "Order number is required"}, status=400)
        if not total_price:
            return JsonResponse({"error": "Total price is required"}, status=400)

        # add new order to db
        new_order = Order.objects.create(
            order_number=order_number,
            total_price=total_price,
            created_time = created_time
        )
        return JsonResponse({"message": "New order added"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    #return HttpResponseBadRequest()