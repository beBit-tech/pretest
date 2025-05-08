from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
from .models import Order  # 確保你已建立 Order model 並正確匯入
from .serializers import OrderSerializer
from django.utils.dateparse import parse_datetime

ACCEPTED_TOKEN = 'omni_pretest_token'

@api_view(['POST'])
def import_order(request):
    # 驗證授權 token
    token = request.headers.get('Authorization')
    if token != ACCEPTED_TOKEN:
        return HttpResponseBadRequest("Invalid token")

    # 解析 JSON 請求資料
    data = request.data
    order_number = data.get('order_number')
    total_price = data.get('total_price')
    created_time = data.get('created_time')

    # 驗證資料完整性
    if not order_number or not total_price or not created_time:
        return HttpResponseBadRequest("Missing required fields")

    try:
        created_time_parsed = parse_datetime(created_time)
        if created_time_parsed is None:
            return HttpResponseBadRequest("Invalid datetime format")

        # 建立 Order 實體並儲存
        order = Order(
            order_number=order_number,
            total_price=total_price,
            created_time=created_time_parsed
        )
        order.save()

        return Response({"message": "Order imported successfully"})

    except Exception as e:
        return HttpResponseBadRequest(f"Error: {str(e)}")

@api_view(['GET'])
def list_orders(request):
    token = request.headers.get('Authorization')
    if token != ACCEPTED_TOKEN:
        return HttpResponseBadRequest("Invalid token")

    order_number = request.query_params.get('order_number')
    if order_number:
        orders = Order.objects.filter(order_number=order_number)
    else:
        orders = Order.objects.all()
    
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)