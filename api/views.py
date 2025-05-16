from textwrap import wrap
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import Comment, Order, Product, ProductSell, Seller
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.serializers import serialize
from datetime import datetime
from rest_framework import status 
from django.views.decorators.csrf import csrf_exempt
from .serialization import *
from functools import wraps


ACCEPTED_TOKEN = ('omni_pretest_token')

def decorator(func):
    @wraps(func)
    def wrapper(request,*args, **kwargs):

        token = request.data.get('token')

        # 驗證 token
        if token != ACCEPTED_TOKEN:
            return HttpResponseBadRequest("invalid or missing token")
        
        return func(request,*args,*kwargs)
    
    return wrapper


@api_view(['POST'])
def import_order(request):
    '''使用POST查詢重要訂單'''
    order_num_ = request.data.get('order_num') 

    token = request.data.get('token')

        # 驗證 token
    if token != ACCEPTED_TOKEN:
        return HttpResponseBadRequest("invalid or missing token")

    # check datatype with query input
    try:
        order_num_ = int(order_num_)
    except TypeError:
        return Response({"error message": "Input data type is invalid."},status=status.HTTP_400_BAD_REQUEST)  # invalid data, return 400

    result = Order.objects.get(order_num = order_num_)
    serialize_order = OrderSerializer(result)

    return Response({"message": f"Order number:{order_num_}","data":serialize_order.data})
    


@api_view(['POST'])
@decorator
def import_order2(request):
    '''使用POST查詢重要訂單 (加上decorator) '''
    order_num_ = request.data.get('order_num') 
    
    # check datatype with query input
    try:
        order_num_ = int(order_num_)
    except TypeError:
        return Response({"error message": "Input data type is invalid."},status=status.HTTP_400_BAD_REQUEST)  # invalid data, return 400

    result = Order.objects.get(order_num = order_num_)
    serialize_order = OrderSerializer(result)

    return Response({"message": f"Order number:{order_num_}","data":serialize_order.data})
    

@api_view(['POST'])
@decorator
def order_detail(request):
    '''搜尋訂單編號，顯示訂單的 detail '''
    order_num_ = request.data.get('order_num')

    sell_list = ProductSell.objects.filter(order__order_num=order_num_)
    sell_result = ProductSellSeriallizer(sell_list,many=True)

    return Response({"order_num":order_num_,"order detail":sell_result.data})



@api_view(['POST'])
def order_feedback(request):
    '''查詢瀏覽訂單評價'''

    order_num_ = request.data.get('order_num') # query ordum number

    comment_list = Comment.objects.filter(order__order_num=order_num_)
    comment_result = CommentSeriallizer(comment_list,many= True)

    return Response({"comment list":comment_result.data})



@api_view(['GET'])
def all_store(request):
    '''Shown the store and seller name'''
    
    all_store = Seller.objects.all()
    all_seller = SellerSeriallizer(all_store,many=True)

    return Response({"message":"Show all store and seller name.", "store_list":all_seller.data})



@api_view(['GET'])
def all_product_from_seller(request, seller_name= None):
    '''進到個人商店，陳列商品'''

    if seller_name!=None:
        all_product = Product.objects.filter(seller__buyeruser__name=seller_name)
        result = ProductSeriallizer(all_product,many=True)
        return Response({"data":result.data})

