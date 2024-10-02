import json
from typing import List
from datetime import datetime

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse

class TestGetAllOrders(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("get_all_orders")
        self.ACCEPTED_TOKEN = ('omni_pretest_token')
        
        self.product_name_1 = "Apple"
        self.product_price_1 = 12.5
        self.product_number_1 = self.__create_product(name = self.product_name_1, price = self.product_price_1)
        
        self.product_name_2 = "Banana"
        self.product_price_2 = 6.5
        self.product_number_2 = self.__create_product(name = self.product_name_2, price = self.product_price_2)
        
    def __create_product(self, name: str, price: float):
        payload = {
                "name": name,
                "price": price
        }
        create_product_url = reverse("create_product")
        response: HttpResponse = self.client.post(create_product_url, data = payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        return response_data["number"]
    
    def __import_order(self, created_time: str, total_price: float, order_lines: List[dict]):
        import_order_url = reverse("import_order")
        valid_payload = {
            "total_price": total_price,
            "created_time": created_time,
            "order_lines": order_lines
        }
        
        response: HttpResponse = self.client.post(import_order_url, data = valid_payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        return response_data["number"]

    def test_get_all_orders(self):
        created_time_1 = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        total_price_1 = 37.5
        quantity_1 = 3
        order_lines_1 = [
            {
                "number": self.product_number_1,
                "quantity": quantity_1
            }
        ]
        order_number_1 = self.__import_order(created_time = created_time_1, total_price = total_price_1, order_lines = order_lines_1)
        created_time_2 = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        total_price_2 = 13
        quantity_2 = 2
        order_lines_2 = [
            {
                "number": self.product_number_2,
                "quantity": quantity_2
            }
        ]
        order_number_2 = self.__import_order(created_time = created_time_2, total_price = total_price_2, order_lines = order_lines_2)
        
        response: HttpResponse = self.client.get(self.url, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data["message"], "Fetch orders successfully.")
        
        self.assertEqual(response_data["orders"][0]["number"], order_number_1)
        self.assertEqual(response_data["orders"][0]["created_time"], created_time_1)
        self.assertEqual(response_data["orders"][0]["total_price"], total_price_1)
        self.assertEqual(response_data["orders"][0]["order_lines"][0]["number"], self.product_number_1)
        self.assertEqual(response_data["orders"][0]["order_lines"][0]["quantity"], quantity_1)
        self.assertEqual(response_data["orders"][1]["number"], order_number_2)
        self.assertEqual(response_data["orders"][1]["created_time"], created_time_2)
        self.assertEqual(response_data["orders"][1]["total_price"], total_price_2)
        self.assertEqual(response_data["orders"][1]["order_lines"][0]["number"], self.product_number_2)
        self.assertEqual(response_data["orders"][1]["order_lines"][0]["quantity"], quantity_2)
        
    def test_get_all_orders_without_token(self):
        response: HttpResponse = self.client.get(self.url, format = "json")
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)