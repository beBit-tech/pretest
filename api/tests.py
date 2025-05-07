from django.test import TestCase
from rest_framework.test import APITestCase


class OrderTestCase(APITestCase):
    def setUp(self):
        self.valid_data = {
            "token": "omni_pretest_token",
            "order_number": "123456",
            "total_price": 100.50,
        }
        self.invalid_token = {
            "token": "invalid_token",
            "order_number": "123456",
            "total_price": 100.50,
        }
        self.missing_token = {
            "order_number": "123456",
            "total_price": 100.50,
        }
        self.invalid_data = {
            "token": "omni_pretest_token",
            "order_number": "",
            "total_price": "not_a_number",
        }

    def test_import_order_success(self):
        response = self.client.post(
            '/api/import-order/',
            data=self.valid_data,
            format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['order_number'], self.valid_data['order_number'])
        self.assertEqual(float(response.json()['total_price']), float(self.valid_data['total_price']))
        self.assertIn('created_time', response.json())
        self.assertIsInstance(response.json()['created_time'], str)
    
    def test_import_order_invalid_token(self):
        response = self.client.post(
            '/api/import-order/',
            data=self.invalid_token,
            format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_import_order_missing_token(self):
        response = self.client.post(
            '/api/import-order/',
            data=self.missing_token,
            format='json')
        self.assertEqual(response.status_code, 401)
    
    def test_import_order_invalid_data(self):
        response = self.client.post(
            '/api/import-order/',
            data=self.invalid_data,
            format='json')
        self.assertEqual(response.status_code, 400)
