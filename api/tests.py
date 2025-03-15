import json

from api.models import Order
from api.views import ACCEPTED_TOKEN
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.client = APIClient()
        self.url = "/api/import-order/"
        self.valid_token = f"Bearer {ACCEPTED_TOKEN}"

    def test_import_order_success(self):
        '''
        測試成功導入訂單
        '''

        # Given
        data = {
            "order_number": "ORDER-1",
            "total_price": 99.99
        }

        # When
        response = self.client.post(
            self.url,
            data,
            HTTP_AUTHORIZATION=self.valid_token
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("successfully", response_data['message'])
        self.assertTrue(Order.objects.filter(order_number="ORDER-1").exists())
        order = Order.objects.get(order_number="ORDER-1")
        self.assertEqual(float(order.total_price), 99.99)

    def test_import_order_invalid_token(self):
        '''
        測試 access token 錯誤
        '''

        # Given, When
        response = self.client.post(
            self.url,
            {"order_number": "ORDER-1", "total_price": 99.99},
            HTTP_AUTHORIZATION="Bearer wrong_token")

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Invalid token')

    test_missing_fields_data = [
        ({}),
        ({"order_number": "ORDER-1"}),
        ({"total_price": 99.99}),
    ]

    def test_import_order_missing_fields(self):
        '''
        測試缺少必要欄位時回傳錯誤
        '''

        for data in self.test_missing_fields_data:
            # Given, When
            response = self.client.post(
                self.url,
                data,
                HTTP_AUTHORIZATION=self.valid_token)

            # Then
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid request data', response.content.decode('utf-8'))
