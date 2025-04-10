from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
import json
from django.http import JsonResponse
from django.utils.timezone import now
from api.models import Order
# Create your views here.


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    # Add your code here
    try:
        # Validating access token from request data, suppose there is a token in post request payload
        data = json.loads(request.body)
        token = data.get('token')

        if token not in ACCEPTED_TOKEN:
            return JsonResponse({"error": "Unauthorized: Invalid token"}, status=401)

        # get order info from json
        order_number = data.get("order_number",'')
        total_price = data.get("total_price",'')
        if not order_number:
            return JsonResponse({"error": "Order number is required"}, status=400)
        if not total_price:
            return JsonResponse({"error": "Total price is required"}, status=400)
        new_order = Order.objects.create(
            order_number=order_number,
            total_price=total_price
        )
        return JsonResponse({"message": "New order added"}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    #return HttpResponseBadRequest()