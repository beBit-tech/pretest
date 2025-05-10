from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Order
from django.urls import reverse

# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here

    def setUp(self):
        self.url = reverse('import-order')
        self.accept_token = 'omni_pretest_token'




    def test_whether_token(self):
        # 測試傳遞的資料不包含 token
        response = self.client.post(
            self.url,
            {
                "order_num":123,
                "total_price":100,
                'created':'2025-05-08'
            },
            format='json'
        )

        self.assertEqual(response.status_code,400)

        # 檢測輸出是否對應正確
        self.assertIn("invalid or missing token",
            response.content.decode()
        )

    def test_not_correct_token(self):

        send_data = {
                "token":"not_onmi_token",
                "order_num":123,
                "total_price":100,
                'created':'2025-05-08'
        }

        response = self.client.post(
            self.url,
            send_data,
            format='json'
        )
        self.assertEqual(response.status_code,400)


    def test_correct_token(self):

        send_data = {
                "token":self.accept_token,
                "order_num":123,
                "total_price":100,
                'created':'2025-05-08'
        }
        response = self.client.post(
            self.url,
            send_data,
            format='json'
        )
        self.assertEqual(response.status_code,200)
        self.assertEqual(Order.objects.count(),1)  # 加入一筆資料檢查

        #  驗證加入資料庫的 data
        get_order = Order.objects.first()
        self.assertEqual(get_order.order_num, send_data['order_num'])
        self.assertEqual(get_order.total_price, send_data['total_price'])

        
    # def test_token_with_decorator(self):
