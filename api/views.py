from django.shortcuts import render
from django.http import HttpResponseBadRequest
from rest_framework.decorators import api_view
from .decorators import token_required
from uuid import UUID
# Create your views here.

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from .models import Order,Product,OrderItem
from django.core.exceptions import ValidationError

from django.db import transaction

@api_view(['POST'])
@token_required
def import_order(request):
    try:
        # 使用事務包裹整個訂單建立流程
        with transaction.atomic():
            # 驗證基本輸入格式
            products_data = request.data.get('products', [])
            if not isinstance(products_data, list):
                return Response({'error': '商品資料格式錯誤，應為陣列[]'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not products_data:
                return Response({'error': '至少需要一項商品'}, status=status.HTTP_400_BAD_REQUEST)

            # 建立訂單物件（先不保存到資料庫）
            order = Order()
            order.full_clean()  # 驗證模型欄位
            order.save()  # 正式建立訂單
            
            errors = []

            for idx, product_data in enumerate(products_data):
                product_id = product_data.get('product_id')
                quantity = product_data.get('quantity', 1)

                # 驗證必要欄位
                if not product_id:
                    errors.append(f"第{idx+1}項商品缺少product_id")
                    continue
                # 驗證UUID格式
                try:
                    uuid_obj = UUID(product_id, version=4)
                except ValueError:
                    errors.append(f"第{idx+1}項商品ID格式錯誤")
                    continue
            
                # 驗證數量格式
                try:
                    quantity = int(quantity)
                    if quantity < 1:
                        errors.append(f"第{idx+1}項商品數量必須大於0")
                except (ValueError, TypeError):
                    errors.append(f"第{idx+1}項商品數量格式錯誤")
                    continue

                # 檢查商品是否存在
                try:
                    product = Product.objects.get(uid=product_id)
                except Product.DoesNotExist:
                    errors.append(f"第{idx+1}項商品不存在 (ID: {product_id})")
                    continue

                # 建立訂單項目
                try:
                    order_item = OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity
                    )
                    order_item.full_clean()  # 驗證模型欄位
                    order_item.save()
                except ValidationError as e:
                    errors.append(f"第{idx+1}項商品資料無效: {', '.join(e.messages)}")

            # 處理驗證錯誤
            if errors:
                transaction.set_rollback(True)
                return Response({'errors': errors}, status=status.HTTP_400_BAD_REQUEST)
            # 手動重新計算總價
            order.refresh_from_db()

    except Exception as e:
        # 捕捉未預期的錯誤
        return Response({'error': f'伺服器錯誤: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 回傳成功響應
    return Response({
        'status': 'successful',
        'order_id': order.id,
        'order_number': str(order.order_number),
        'total_price': order.total_price
    }, status=status.HTTP_201_CREATED)
