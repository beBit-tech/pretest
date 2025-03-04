from datetime import datetime

from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def test_create_order_successfully(self) -> None:
        data = {
            "access_token": "omni_pretest_token",
            "order_number": 12345,
            "total_price": "99.99",
        }

        response = self.client.post("/api/import-order/", data, format="json")
        order_data = response.json()["order"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order_data["order_number"], 12345)
        self.assertEqual(order_data["total_price"], "99.99")

        created_time = order_data["created_time"]
        self.assertIsNotNone(created_time)
        datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S.%fZ")

    def test_invalid_token(self) -> None:
        """Test with invalid access token"""
        data = {
            "access_token": "wrong_token",
            "order_number": 12345,
            "total_price": "99.99",
        }

        response = self.client.post("/api/import-order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"error": "Invalid access token"})

    def test_missing_token(self) -> None:
        """Test with missing access token"""
        data = {
            "order_number": 12345,
            "total_price": "99.99",
        }

        response = self.client.post("/api/import-order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {"error": "Invalid access token"})

    def test_missing_order_number(self) -> None:
        """Test with missing required fields"""
        data = {
            "access_token": "omni_pretest_token",
            "total_price": "99.99",
        }

        response = self.client.post("/api/import-order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("order_number", response.json()["error"])

    def test_missing_total_price(self) -> None:
        """Test with missing required fields"""
        data = {
            "access_token": "omni_pretest_token",
            "order_number": 12345,
        }

        response = self.client.post("/api/import-order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("total_price", response.json()["error"])

    def test_duplicate_order_number(self) -> None:
        data = {
            "access_token": "omni_pretest_token",
            "order_number": 12345,
            "total_price": "99.99",
        }

        # Create first order
        self.client.post("/api/import-order/", data, format="json")

        # Try to create second order with same number
        response = self.client.post("/api/import-order/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("order_number", response.json()["error"])
