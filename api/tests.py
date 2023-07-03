from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Order

class OrderTestCase(APITestCase):
    def test_import_order(self):
        url = reverse('import_order')
        data = {
            'order_number': '12345',
            'total_price': 100.00,
            'created_time': '2023-07-01T00:00:00Z',
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION='omni_pretest_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().order_number, '12345')