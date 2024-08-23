from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Order


class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('import_order')
        self.valid_token = 'omni_pretest_token'
        self.headers = {'Authorization': self.valid_token}

    def test_import_order_success(self):
        data = {
            'order_number': '12345',
            'total_price': '100.50'
        }
        response = self.client.post(self.url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Order.objects.filter(order_number='12345').exists())

    def test_import_order_invalid_token(self):
        data = {
            'order_number': '12345',
            'total_price': '100.50'
        }
        response = self.client.post(self.url, data, format='json', HTTP_AUTHORIZATION='invalid_token')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_import_order_missing_fields(self):
        data = {
            'order_number': '12345'
        }
        response = self.client.post(self.url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_order_duplicate_order_number(self):
        Order.objects.create(order_number='12345', total_price=100.50)
        data = {
            'order_number': '12345',
            'total_price': '200.00'
        }
        response = self.client.post(self.url, data, format='json', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)