from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order
from datetime import datetime
import pytz


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.token = 'omni_pretest_token'
        self.valid_payload = {
            "order_number": "ORDER123",
            "total_price": "199.99",
            "created_time": "2024-01-01T12:00:00Z"
        }
        self.headers = {'HTTP_AUTHORIZATION': self.token}

    def test_create_order_success(self):
        url = reverse('import_order')
        response = self.client.post(url, self.valid_payload, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, "ORDER123")

    def test_create_order_missing_token(self):
        url = reverse('import_order')
        response = self.client.post(url, self.valid_payload, format='json')  # 沒帶 token
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_missing_fields(self):
        url = reverse('import_order')
        payload = {
            "order_number": "ORDER124",
            # 少了 total_price 和 created_time
        }
        response = self.client.post(url, payload, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_orders_success(self):
        # 先建立一筆訂單
        Order.objects.create(
            order_number="ORDER999",
            total_price=99.99,
            created_time=pytz.UTC.localize(datetime(2024, 1, 1, 12, 0))
        )

        url = reverse('list_orders')
        response = self.client.get(url, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['order_number'], "ORDER999")

    def test_get_orders_missing_token(self):
        url = reverse('list_orders')
        response = self.client.get(url)  # 沒帶 token
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    