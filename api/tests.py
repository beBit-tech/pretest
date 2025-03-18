from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from api.models import Order
import json

ACCEPTED_TOKEN = "omni_pretest_token"

class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('import_order')
        self.valid_token = f"Bearer {ACCEPTED_TOKEN}"
        self.valid_order = {
            "Order_number": "ORD123456",
            "Total_price": "99.99",
            "Customer_name": "John Doe",
            "Status": "Pending"
        }
        self.invalid_order = {
            "Order_number": "ORD123456"
        }

    def test_import_order_success(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_order),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.valid_token
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.first().Order_number, "ORD123456")

    def test_import_order_unauthorized(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.valid_order),
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer wrong_token"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_import_order_missing_fields(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.invalid_order),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.valid_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_order_invalid_json(self):
        response = self.client.post(
            self.url,
            data="invalid json",
            content_type="application/json",
            HTTP_AUTHORIZATION=self.valid_token
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    pass