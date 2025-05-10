from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
# from .permission import TokenValid



ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['GET','POST'])
def import_order(request):
    if request.method=='POST':
        # 從 request.data 中獲取 token
        token = request.data.get('token')

        # 驗證 token
        if token != ACCEPTED_TOKEN:
            return HttpResponseBadRequest("invalid or missing token")
        
        # 取得不同欄位的對應資料
        order_num_ = request.data.get('order_num')
        total_price_ = request.data.get('total_price')
        created_ = request.data.get('created')

        Order.objects.using("default")
        get_order = Order(order_num =order_num_,total_price= total_price_,created=created_)
        get_order.save()

        # 儲存資料到

        # 如果 token 驗證成功，繼續處理請求
        return Response({"message": "Got some data!","data": request.data})
    # Add your code here
    return Response({"message": "Hello, world!"})


