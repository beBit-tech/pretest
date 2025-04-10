from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Order
from rest_framework import status

# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.url = reverse('import_order')
        self.valid_token = 'omni_pretest_token'

    # Test success cases
    def test_success_with_created_time(self):
        data = {
            'token': self.valid_token,
            'order_number': 'ORD0001',
            'total_price': 100.00,
            'created_time': '2025-04-10T15:30:00Z'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, 'ORD0001')

    def test_success_without_created_time(self):
        data = {
            'token': self.valid_token,
            'order_number': 'ORD0002',
            'total_price': 200.00
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().order_number, 'ORD0002')

    # Test error cases
    def test_invalid_token(self):
        data = {
            'token': 'wrong_token',
            'order_number': 'ORD0003',
            'total_price': 300.00,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), 0)

    def test_missing_token(self):
        data = {
            'order_number': 'ORD0004',
            'total_price': 400.00,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Order.objects.count(), 0)

    def test_missing_order_number(self):
        data = {
            'token': self.valid_token,
            'total_price': 500.00,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_missing_total_price(self):
        data = {
            'token': self.valid_token,
            'order_number': 'ORD0006',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_time_format(self):
        data = {
            'token': self.valid_token,
            'order_number': 'ORD0007',
            'total_price': 700.00,
            'created_time':'invalid-date'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)