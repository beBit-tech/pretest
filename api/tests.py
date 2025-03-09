from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product, Order


class OrderTestCase(APITestCase):

    def setUp(self):
        self.product1 = Product.create_product(name="Product 1", price=10.00)
        self.product2 = Product.create_product(name="Product 2", price=20.00)
        self.valid_payload = {
            "token": "omni_pretest_token",
            "total_price": 30.00,
            "products": [self.product1.id, self.product2.id]
        }
        self.invalid_token_payload = {
            "token": "invalid_token",
            "total_price": 30.00,
            "products": [self.product1.id, self.product2.id]
        }
        self.missing_fields_payload = {
            "token": "omni_pretest_token",
            "total_price": 30.00
        }
        self.invalid_product_ids_payload = {
            "token": "omni_pretest_token",
            "total_price": 30.00,
            "products": [999, 1000]
        }
        self.wrong_total_price_payload = {
            "token": "omni_pretest_token",
            "total_price": 25.00,
            "products": [self.product1.id, self.product2.id]
        }
        self.import_order_url = reverse('import_order')

    def test_create_order_with_valid_payload(self):
        response = self.client.post(self.import_order_url, self.valid_payload, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get(order_number=response_data['order_number']).total_price, 30.00)

    def test_create_order_with_invalid_token(self):
        response = self.client.post(self.import_order_url, self.invalid_token_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_missing_fields(self):
        response = self.client.post(self.import_order_url, self.missing_fields_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_with_invalid_product_ids(self):
        response = self.client.post(self.import_order_url, self.invalid_product_ids_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_order_with_wrong_total_price(self):
        response = self.client.post(self.import_order_url, self.wrong_total_price_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)