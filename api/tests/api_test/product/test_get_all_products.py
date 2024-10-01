import json
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.http import HttpResponse

class TestGetAllProducts(APITestCase):
    
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("get_all_products")
        self.ACCEPTED_TOKEN = ('omni_pretest_token')
        
        self.valid_payload_1 = {
            "name": "Apple",
            "price": 12.5
        }
        self.valid_payload_2 = {
            "name": "Banana",
            "price": 6.5
        }

    def __create_product(self, payload: dict):
        url = reverse("create_product")
        response = self.client.post(url, data = payload, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))

        return response_data["number"]

    def test_get_all_products(self):
        product_number_1 = self.__create_product(payload = self.valid_payload_1)
        product_number_2 = self.__create_product(payload = self.valid_payload_2)
        
        response: HttpResponse = self.client.get(self.url, format = "json", HTTP_AUTHORIZATION = self.ACCEPTED_TOKEN)
        response_data = json.loads(response.content.decode('utf-8'))
        
        self.assertEqual(response_data["products"][0]["number"], product_number_1)
        self.assertEqual(response_data["products"][0]["name"], self.valid_payload_1["name"])
        self.assertEqual(response_data["products"][0]["price"], self.valid_payload_1["price"])
        self.assertEqual(response_data["products"][1]["number"], product_number_2)
        self.assertEqual(response_data["products"][1]["name"], self.valid_payload_2["name"])
        self.assertEqual(response_data["products"][1]["price"], self.valid_payload_2["price"])