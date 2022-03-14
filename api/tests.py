import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework import status
from api.models import *

# Create your tests here.
class OrderTestCase(APITestCase):
    def setUp(self) -> None:
        self.client.credentials(HTTP_AUTHORIZATION=settings.ACCEPTED_TOKEN)
        self.product1, self.product2 = Product.objects.bulk_create(
            [Product(name=f"product{i}", price=100, amount=10, status=True) for i in range(1, 3)]
        )

    def test_import_order(self):
        url = reverse("import_order")
        order_detail = {self.product1.id: 1, self.product2.id: 10}
        data = {"products": json.dumps(order_detail)}
        response = self.client.post(url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 判斷回傳200
        created_order = Order.objects.first()
        self.assertIsNotNone(created_order)  # 判斷資料庫有資料
        self.assertEqual(response_data["order_number"], created_order.order_number)  # 判斷回傳的訂單編號等於資料庫的訂單編號
        self.assertEqual(
            response_data["total_price"],
            self.product1.price * order_detail[self.product1.id] + self.product2.price * order_detail[self.product2.id],
        )  # 判斷回傳的總價等於資料庫的總價
        self.assertEqual(
            created_order.products.get(id=self.product1.id).amount,
            self.product1.amount - order_detail[self.product1.id],
        )  # 判斷商品庫存是否減少
        self.assertEqual(created_order.products.get(id=self.product2.id).amount, False)  # 判斷商品狀態是否會自動變成False

        # 判斷下架商品是否不能再次下單
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 判斷ID不存在報錯
        order_detail[self.product2.id + 1] = 1
        data = {"products": json.dumps(order_detail)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        order_detail.popitem()

        # 判斷商品庫存不足報錯
        order_detail[self.product1.id] = 11
        data = {"products": json.dumps(order_detail)}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 判斷停用驗證報錯
        self.client.credentials()
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # 判斷回傳401
