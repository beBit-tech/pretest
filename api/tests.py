from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Order
import uuid  

# Import-order test cases
class OrderTestCase(APITestCase):

    def setUp(self):
        self.url = '/api/import-order/'
        self.valid_token = 'omni_pretest_token'
        self.invalid_token = 'invalid_token'
        self.valid_order_data = {
            'order_number': str(uuid.uuid4()),
            'total_price': 10.0,
        }
        self.invalid_order_data = {
            'order_number': str(uuid.uuid4()),
        }

    def test_import_order_success(self):
        response = self.client.post(
            self.url, 
            self.valid_order_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token
        )
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertEqual(response.data['total_price'], 10.0)

        # Verify if the order has been saved to the database
        order = Order.objects.get(id=response.data['order_id'])
        self.assertEqual(order.total_price, self.valid_order_data['total_price'])

    def test_import_order_invalid_token(self):
        response = self.client.post(self.url, self.valid_order_data,
                                     HTTP_AUTHORIZATION=self.invalid_token)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"error": "Invalid token"})

    def test_import_order_no_data(self):
        response = self.client.post(self.url, {}, 
                                     HTTP_AUTHORIZATION=self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "No order data provided"})

    def test_import_order_invalid_data(self):
        response = self.client.post(self.url, self.invalid_order_data, 
                                     HTTP_AUTHORIZATION=self.valid_token)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("total_price", response.data)