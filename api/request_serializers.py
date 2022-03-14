import traceback
from rest_framework import serializers
from api.models import *
from django.db import transaction


class ImoprtOrderSerializer(serializers.Serializer):
    class Meta:
        model = Order
        fields = ("products",)

    products = serializers.JSONField(
        help_text="""商品ID以及對應的購買數量
            限定輸入`Json`
            格式 `{商品ID: 商品數量, ...}`
            e.g {"1": 2, "2": 1}""",
    )

    def create(self, validated_data):
        try:
            with transaction.atomic():
                total_price = 0
                order = Order.objects.create(total_price=total_price)
                for product_id, quantity in validated_data["products"].items():
                    product = Product.objects.select_for_update().get(id=product_id)  # 加上select_for_update，防止併發
                    if product.amount < quantity:
                        raise serializers.ValidationError(f"商品ID {product_id} 數量不足")
                    elif product.status is False:
                        raise serializers.ValidationError(f"商品ID {product_id} 已下架")
                    total_price += product.price * quantity  # 商品價格 * 購買數量
                    # 減少商品庫存
                    product.amount -= quantity
                    # 如果商品庫存為0，將商品狀態設為False(下架)
                    if product.amount == 0:
                        product.status = False
                    product.save()
                    OrderProduct.objects.create(order=order, product=product, quantity=quantity)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"商品ID {product_id} 不存在")
        except serializers.ValidationError as error_message:
            raise error_message
        except Exception:
            print(traceback.format_exc())
            raise serializers.ValidationError("訂單建立失敗，請稍後再試")

        else:
            # 更新訂單總金額
            order.total_price = total_price
            order.save()
            return order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
