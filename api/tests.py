import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Order, Product


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here

    def setUp(self):
        self.valid_token = "omni_pretest_token"
        self.invalid_token = "wrong_token"

        # Create test products
        self.product1 = Product.objects.create(name = "Laptop", price = 999.99, stock = 5)
        self.product2 = Product.objects.create(name = "Mouse", price = 9.99, stock = 20)

        self.base_valid_data = {
            "order_number": "ORD12345",
            "total_price": 1009.98,
            "customer_name": "Test test",
            "customer_email": "Test@example.com",
            "product_ids": [self.product1.id, self.product2.id]
        }

        self.url = "/api/import_order/"

    def send_request(self, data):
        return self.client.post(
            path = self.url,
            data = json.dumps(data),
            content_type = "application/json",
            HTTP_AUTHORIZATION = self.valid_token
        )

    def test_import_order_success(self):
        response = self.send_request(self.base_valid_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_missing_order_number(self):
        data = self.base_valid_data.copy()
        del data["order_number"]
        response = self.send_request(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_total_price(self):
        data = self.base_valid_data.copy()
        del data["total_price"]
        response = self.send_request(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_customer_name(self):
        data = self.base_valid_data.copy()
        del data["customer_name"]
        response = self.send_request(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_customer_email(self):
        data = self.base_valid_data.copy()
        del data["customer_email"]
        response = self.send_request(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_product_ids(self):
        data = self.base_valid_data.copy()
        del data["product_ids"]
        response = self.send_request(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_import_order_invalid_token(self):
        response = self.client.post(
            path=self.url,
            data=json.dumps(self.base_valid_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=self.invalid_token
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
