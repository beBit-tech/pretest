from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Order
from rest_framework import status


# Create your tests here.
class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = '/api/import_order/'
        self.valid_token = 'omni_pretest_token'

    def test_valid_order_creation(self):
        data = {
            "access_token": self.valid_token,
            "order_number": "ORDER1",
            "total_price": "199.49"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().order_number, "ORDER1")

    def test_valid_token(self):
        data = {
            "access_token": "Wrong_token",
            "order_number": "ORDER2",
            "total_price": "299.49"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_missing_fields(self):
        data = {
            "access_token": self.valid_token,
            "order_number": "ORDER3",
            # missing price
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    