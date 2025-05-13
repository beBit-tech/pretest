from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import Order
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core import serializers
from datetime import datetime
from rest_framework import status 


ACCEPTED_TOKEN = ('omni_pretest_token')


@api_view(['POST'])
def import_order(request):
    '''使用POST查詢重要訂單'''

    token = request.data.get('token')

        # 驗證 token
    if token != ACCEPTED_TOKEN:
        return HttpResponseBadRequest("invalid or missing token")
    
    # 取得不同欄位的對應資料
    order_num_ = request.data.get('order_num')  # query input 
    # total_price_ = request.data.get('total_price')
    # created_ = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # system generate


    try:
        order_num_ = int(order_num_)

        result = Order.objects.get(order_num = order_num_)
        return Response({"message": "Got some data!","data": serializers.serialize('json',result)})

    except TypeError:
        return Response({"error message": "Input data type is invalid."},status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_order(request):

    
    s_order = serializers.serialize('json', Order.objects.all()) 

    return Response({"data":s_order})

