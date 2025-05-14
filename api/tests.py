from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.shortcuts import reverse
from .models import Order, Product, OrderItem
import uuid

class OrderImportTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # 建立測試用商品
        cls.valid_product = Product.objects.create(
            uid=uuid.UUID('550e8400-e29b-41d4-a716-446655440000'),
            name='測試商品',
            price=1000
        )

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('import-order')
        self.valid_payload = {
            'access_token': 'omni_pretest_token',
            'products': [
                {
                    'product_id': '550e8400-e29b-41d4-a716-446655440000',
                    'quantity': 2
                }
            ]
        }
    # --------------------------
    # 成功案例測試
    # --------------------------
    def test_successful_order(self):
        """測試成功的訂單匯入"""
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('order_id', response.data)
    
    # --------------------------
    # 授權驗證測試
    # --------------------------
    def test_missing_access_token(self):
        """測試缺少access_token"""
        invalid_payload = {
            'products': self.valid_payload['products']
        }
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('缺少token', response.data['error'])

    def test_invalid_access_token(self):
        """測試錯誤access_token值"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['access_token'] = 'wrong_token'
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('無效token', response.data['error'])

    # --------------------------
    # 商品數據結構驗證測試
    # --------------------------
    def test_empty_products_list(self):
        """測試空商品陣列"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'] = []
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('至少需要一項商品', response.data['error'])

    def test_invalid_products_type(self):
        """測試非陣列型態的products字段"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'] = 'not_a_list'
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('應為陣列', response.data['error'])

    # --------------------------
    # 商品項目驗證測試
    # --------------------------
    def test_missing_product_id(self):
        """測試商品缺少product_id"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'] = [{'quantity': 2}]
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('缺少product_id', response.data['errors'][0])

    def test_nonexistent_product(self):
        """測試不存在的商品ID"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'] = [{'product_id': '550e8400-e29b-41d4-a716-446655441234', 'quantity': 1}]
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('商品不存在', response.data['errors'][0])

    def test_invalidUUID_product(self):
        """測試無效的UUID"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'] = [{'product_id': 'invalid_UUID', 'quantity': 1}]
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('ID格式錯誤', response.data['errors'][0])
    # --------------------------
    # 數量驗證測試
    # --------------------------
    def test_zero_quantity(self):
        """測試商品數量為0"""
        invalid_payload = self.valid_payload.copy()
        invalid_payload['products'][0]['quantity'] = 0
        response = self.client.post(self.url, invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



