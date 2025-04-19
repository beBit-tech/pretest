from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order
import json
from decimal import Decimal


# Create your tests here.
class OrderTestCase(APITestCase):
    valid_token = 'omni_pretest_token'

    def setUp(self):
        self.response = None
        self.data = {}

    def test_import_order_without_token_and_missing_data(self):
        self.response = self._call_import_order(self.data)
        
        self._response_status_code_should_be(status.HTTP_401_UNAUTHORIZED)
        self._order_should_not_create()

    def test_import_order_with_invalid_token_and_missing_data(self):
        self._given_token('invalid_token')

        self.response = self._call_import_order(self.data)
        
        self._response_status_code_should_be(status.HTTP_401_UNAUTHORIZED)
        self._order_should_not_create()

    def test_import_order_with_valid_token_and_missing_data(self):
        self._given_token(self.valid_token)

        self.response = self._call_import_order(self.data)
        
        self._response_status_code_should_be(status.HTTP_400_BAD_REQUEST)

    def test_import_order_with_valid_token_and_valid_data(self):
        self._given_token(self.valid_token)
        self._given_order_number('ORD-001')
        self._given_total_price(100.00)

        self.response = self._call_import_order(self.data)

        self._response_status_code_should_be(status.HTTP_201_CREATED)
        self._order_should_create()
        self._order_number_should_be('ORD-001')
        self._total_price_should_be(100.00)

    def test_import_order_with_valid_token_and_invalid_data_type(self):
        self._given_token(self.valid_token)
        self._given_order_number('ORD-001')
        self._given_total_price('invalid_total_price')

        self.response = self._call_import_order(self.data)

        self._response_status_code_should_be(status.HTTP_400_BAD_REQUEST)
        self._order_should_not_create()

    def test_import_order_with_valid_token_and_invalid_total_price_range(self):
        self._given_token(self.valid_token)
        self._given_order_number('ORD-001')
        self._given_total_price(-100.00)

        self.response = self._call_import_order(self.data)

        self._response_status_code_should_be(status.HTTP_400_BAD_REQUEST)
        self._order_should_not_create()


    def _given_order_number(self, order_number):
        self.data['order_number'] = order_number

    def _given_total_price(self, total_price):
        self.data['total_price'] = total_price

    def _given_token(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def _call_import_order(self, data):
        return self.client.post('/api/import-order/',data=json.dumps(data), content_type='application/json')
    
    def _response_status_code_should_be(self, expected_status_code):
        self.assertEqual(self.response.status_code, expected_status_code)
    
    def _order_should_not_create(self):
        self.assertEqual(Order.objects.count(), 0)

    def _order_should_create(self):
        self.assertEqual(Order.objects.count(), 1)

    def _order_number_should_be(self, order_number):
        actual_order_number = Order.objects.first().order_number
        self.assertEqual(actual_order_number, order_number)

    def _total_price_should_be(self, total_price):
        actual_total_price = Order.objects.first().total_price
        self.assertEqual(actual_total_price, total_price)