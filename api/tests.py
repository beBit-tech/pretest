from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order
import json


# Create your tests here.
class OrderTestCase(APITestCase):
    def test_import_order_with_invalid_token(self):
        data = {
            'token': 'invalid_token',
            'order_number': 'ORD-001',
            'total_price': 100.00
        }

        response = self.client.post('/api/import-order/', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 0)

    def test_import_order_with_valid_token(self):
        data = {
            'token': 'omni_pretest_token',
            'order_number': 'ORD-001',
            'total_price': 100.00
        }
        
        response = self.client.post('/api/import-order/', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.order_number, 'ORD-001')
        self.assertEqual(float(order.total_price), 100.00)
        
    def test_import_order_with_missing_data(self):
        data = {
            'token': 'omni_pretest_token',
            'order_number': 'ORD-002'
        }

        response = self.client.post('/api/import-order/', data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)