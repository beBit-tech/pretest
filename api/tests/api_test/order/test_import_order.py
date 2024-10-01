import json, uuid
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse

from api.adapter.repository.order.order_model import Order, OrderProduct

class ImportOrderTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("import_order")
        self.ACCEPTED_TOKEN = ('omni_pretest_token')
        self.product_number_1 = self.__create_product(
            payload = {
            "name": "Apple",
            "price": 12.5
            }
        )
        self.product_number_2 = self.__create_product(
            payload = {
            "name": "Banana",
            "price": 6.5
            }
        )
        
    def __create_product(self, payload: dict):
        create_product_url = reverse("create_product")
        response: HttpResponse = self.client.post(create_product_url, data = payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        return response_data["number"]
    
    def test_import_order(self):
        valid_payload = {
            "total_price": 44.5,
            "created_time": "2024-10-01T10:00:00",
            "order_lines": [
                {
                    "number": self.product_number_1,
                    "quantity": 2
                },
                {
                    "number": self.product_number_2,
                    "quantity": 3
                }
            ]
        }
        
        response: HttpResponse = self.client.post(self.url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        response_data = json.loads(response.content.decode('utf-8'))
        order_number = response_data["order_number"]
        order = Order.objects.filter(number = order_number).first()
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_number", response_data)
        self.assertEqual(response_data["message"], "Order created successfully.")
        self.assertIsNotNone(order)

        order_product_1 = OrderProduct.objects.filter(order_number = order_number).first()
        self.assertIsNotNone(order_product_1)
        self.assertEqual(order_product_1.product_number.number, self.product_number_1)
        self.assertEqual(order_product_1.quantity, 2)
        self.assertEqual(order_product_1.product_number.name, "Apple")
        self.assertEqual(order_product_1.product_number.price, 12.5)

        order_product_2 = OrderProduct.objects.filter(order_number = order_number).last()
        self.assertIsNotNone(order_product_2)
        self.assertEqual(order_product_2.product_number.number, self.product_number_2)
        self.assertEqual(order_product_2.quantity, 3)
        self.assertEqual(order_product_2.product_number.name, "Banana")
        self.assertEqual(order_product_2.product_number.price, 6.5)
        
    def test_import_order_with_non_existent_product_number(self):
        valid_payload = {
            "total_price": 25,
            "created_time": "2024-10-01T10:00:00",
            "order_lines": [
                {
                    "number": str(uuid.uuid4()),
                    "quantity": 2
                },
            ]
        }
        
        response: HttpResponse = self.client.post(self.url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_import_order_without_token(self):
        valid_payload = {
            "total_price": 25,
            "created_time": "2024-10-01T10:00:00",
            "order_lines": [
                {
                    "number": self.product_number_1,
                    "quantity": 2
                },
            ]
        }
        
        response = self.client.post(self.url, data = valid_payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_create_product_with_invalid_outter_data(self):
        invalid_payload = {
            "total_price": 25,
            "created_time": "",
            "order_lines": [
                {
                    "number": self.product_number_1,
                    "quantity": 2
                },
            ]
        }
        response = self.client.post(self.url, data = invalid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_product_with_invalid_inner_data(self):
        invalid_payload = {
            "total_price": 25,
            "created_time": "2024-10-01T10:00:00",
            "order_lines": [
                {
                    "number": "",
                    "quantity": 2
                },
            ]
        }
        response = self.client.post(self.url, data = invalid_payload, format="json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)