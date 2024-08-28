from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Order, Product, ProductOrder

class OrderTestCase(APITestCase):
    def setUp(self):
        self.import_order_url = reverse('import_order')
        self.product1 = Product.objects.create(name='Product 1', price=5000, amount=10)
        self.product2 = Product.objects.create(name='Product 2', price=3000, amount=15)
        self.valid_payload = {
            'order_number': 'ORD-001',
            'total_price': 13000,
            'products': [
                {'product_id': self.product1.id, 'quantity': 2},
                {'product_id': self.product2.id, 'quantity': 1}
            ]
        }
        self.valid_token = 'omni_pretest_token'
        self.invalid_token = 'def_not_omni_pretest_token'

    def test_import_order_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)
        response = self.client.post(self.import_order_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
        self.assertIn('order', response.data)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(ProductOrder.objects.count(), 2)
        self.assertEqual(Order.objects.get().order_number, 'ORD-001')

    def test_import_order_missing_token(self):
        response = self.client.post(self.import_order_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Token missing'})

    def test_import_order_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.invalid_token)
        response = self.client.post(self.import_order_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {'error': 'Unauthorized'})
    
    def test_import_order_missing_fields(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)
        invalid_payload = self.valid_payload.copy()
        del invalid_payload['order_number']
        response = self.client.post(self.import_order_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order_number', response.data)

    def test_import_order_invalid_total_price(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)
        invalid_payload = self.valid_payload.copy()
        invalid_payload['total_price'] = -100  
        response = self.client.post(self.import_order_url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('total_price', response.data)

    def test_import_order_duplicate_order_number(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.valid_token)
        self.client.post(self.import_order_url, self.valid_payload, format='json')
        response = self.client.post(self.import_order_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('order_number', response.data)