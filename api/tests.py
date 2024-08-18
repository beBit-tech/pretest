from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Order


# Create your tests here.
class OrderTestCase(APITestCase):
    def setUp(self):

        self.url = reverse("import_order")
        self.valid_token = "omni_pretest_token"
        self.invail_token = "invail_token"
        self.valid_data = {"order_number": "ORD20240818012911", "total_price": "10000"}
        self.invail_data = {"order_number": "", "total_price": "10000"}

    def test_import_order_with_valid_token_and_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("order_id", response.data)
        self.assertEqual(Order.objects.count(), 1)

    def test_import_order_with_invalid_token(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.invail_token,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 0)

    def test_import_order_with_missing_token(self):
        response = self.client.post(self.url, self.valid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Order.objects.count(), 0)

    def test_import_order_with_invalid_data(self):
        response = self.client.post(
            self.url,
            self.invail_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
