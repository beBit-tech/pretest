import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse

from api.adapter.repository.product.product_model import Product

class CreateProductTest(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("create_product")
        self.ACCEPTED_TOKEN = ('omni_pretest_token')

    def test_create_product(self):
        valid_payload = {
            "name": "Apple",
            "price": 12.5
        }
        
        response: HttpResponse = self.client.post(self.url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        product = Product.objects.filter(number = response_data["product_number"]).first()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("product_number", response_data)
        self.assertEqual(response_data["message"], "Product created successfully.")
        self.assertIsNotNone(product)
        self.assertEqual(product.price, 12.5)

    def test_create_exist_product(self):
        valid_payload = {
            "name": "Apple",
            "price": 12.5
        }
        self.client.post(self.url, data = valid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response = self.client.post(self.url, data = valid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_product_with_invalid_data(self):
        invalid_payload = {
            "name": "",
            "price": 12.5
        }
        response = self.client.post(self.url, data = invalid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_product_with_negative_price(self):
        invalid_payload = {
            "name": "",
            "price": -12.5
        }
        response = self.client.post(self.url, data = invalid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_product_without_token(self):
        valid_payload = {
            "name": "Apple",
            "price": 12.5
        }
        
        response = self.client.post(self.url, data = valid_payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
