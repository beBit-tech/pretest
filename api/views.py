from django.shortcuts import render
from django.http import HttpResponseBadRequest, JsonResponse
from rest_framework.decorators import api_view
from .models import Order
from .decorators import require_token
import json

ACCEPTED_TOKEN = ('omni_pretest_token')

'''
# API Token 驗證部份
@api_view(['POST'])
def import_order(request):
    token = request.headers.get("Authorization")
    if not token or token.split(" ")[1] != ACCEPTED_TOKEN:
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        data = json.loads(request.body)
        if "Order_number" not in data or "Total_price" not in data:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        order = Order.objects.create(
            Order_number=data["Order_number"],
            Total_price=data["Total_price"]
        )

        return JsonResponse({"message": "Order created", "order_id": order.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest()
'''

# 使用 Decorator
@api_view(['POST'])
@require_token  
def import_order(request):
    try:
        data = json.loads(request.body)

        if "Order_number" not in data or "Total_price" not in data:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        order = Order.objects.create(
            Order_number=data["Order_number"],
            Total_price=data["Total_price"],
            Customer_name=data.get("Customer_name", ""),
            Status=data.get("Status", "Pending")
        )

        return JsonResponse({"message": "Order created", "order_id": order.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return HttpResponseBadRequest()