from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Order
from rest_framework import status

# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def test_create_order(self):
    #Ensure we can create a new order object.
        url = reverse('order-list')
        data = {"Created_time": "2022-03-06T22:14:22.919665+08:00",
        "Detail": "logitech mouse * 2",
        "Order_number": "d9ebbb63-b171-4c70-9014-6e160eb0f9f4",
        "Total_price": 400,
        "product": 3}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)