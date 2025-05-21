from django.test import TestCase
from rest_framework.test import APITestCase


# Create your tests here.
from rest_framework import status
from .models import Order

class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = '/api/import-order/'
        self.valid_payload = {
            'token': 'omni_pretest_token',
            'order_number': 'ORD001',
            'total_price': '120.00'
        }
        self.invalid_token_payload = {
            'token': 'wrong_token',
            'order_number': 'ORD001',
            'total_price': '120.00'
        }
        self.missing_data_payload = {
            'token': 'omni_pretest_token',
            'order_number': '',
            'total_price': ''
        }

    def test_import_order_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, 'ORD001')

    def test_import_order_unauthorized(self):
        response = self.client.post(self.url, self.invalid_token_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_import_order_missing_data(self):
        response = self.client.post(self.url, self.missing_data_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)