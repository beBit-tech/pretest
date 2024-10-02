import json, uuid
from datetime import datetime

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse
from api.adapter.repository.order.order_model import Order, OrderProduct
from api.adapter.repository.product.product_model import Product

class TestDeleteOrder(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("delete_order")
        self.ACCEPTED_TOKEN = ('omni_pretest_token')
        
        self.product_number = self.__create_product()
        
    def __create_product(self) -> str:
        valid_payload = {
                "name": "Apple",
                "price": 12.5
        }
        create_product_url = reverse("create_product")
        response: HttpResponse = self.client.post(create_product_url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        return response_data["number"]
    
    def __import_order(self) -> str:
        import_order_url = reverse("import_order")
        valid_payload = {
            "total_price": 37.5,
            "created_time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "order_lines": [
                {
                    "number": self.product_number,
                    "quantity": 3
                }
            ]
        }
        
        response: HttpResponse = self.client.post(import_order_url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        return response_data["number"]

    def test_delete_exist_order(self):
        order_number = self.__import_order()
        
        valid_payload = {
            "number": order_number
        }
        
        response: HttpResponse = self.client.delete(self.url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Delete order successfully.")
        
        order = Order.objects.filter(number = order_number).first()
        order_product = OrderProduct.objects.filter(order_number = order_number).first()

        self.assertIsNone(order)
        self.assertIsNone(order_product)
        
        product = Product.objects.filter(number = self.product_number).first()
        
        self.assertIsNotNone(product)
        
    def test_delete_non_existent_order(self):
        _ = self.__import_order()
        
        valid_payload = {
            "number": str(uuid.uuid4)
        }
        
        response: HttpResponse = self.client.delete(self.url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data["message"], "Delete order failed.")
        
    def test_delete_order_without_number(self):
        _ = self.__import_order()
        
        invalid_payload = {
            "number": ""
        }
        
        response: HttpResponse = self.client.delete(self.url, data = invalid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)

        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_delete_order_without_token(self):
        order_number = self.__import_order()
        valid_payload = {
            "number": order_number
        }
        
        response = self.client.post(self.url, data = valid_payload, format="json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        