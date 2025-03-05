from datetime import datetime, timezone

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

        time_before_request = datetime.now(timezone.utc)
        response = self.client.post("/api/import-order/", data, format="json")
        time_after_request = datetime.now(timezone.utc)

        order_data = response.json()["order"]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(order_data["order_number"], 12345)
        self.assertEqual(order_data["total_price"], "99.99")

        created_time = order_data["created_time"]
        self.assertIsNotNone(created_time)
        created_time = datetime.strptime(created_time, "%Y-%m-%dT%H:%M:%S.%fZ").replace(
            tzinfo=timezone.utc
        )
        self.assertGreaterEqual(created_time, time_before_request)
        self.assertLessEqual(created_time, time_after_request)

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


class ProductTestCase(APITestCase):
    def setUp(self) -> None:
        self.test_product = "Test Product"
        self.test_description = "Test Description"
        self.test_price = "29.99"

        self.product_data = {
            "name": self.test_product,
            "description": self.test_description,
            "price": self.test_price,
        }

    def test_create_product_successfully(self) -> None:
        time_before_request = datetime.now(timezone.utc)
        response = self.client.post("/api/products/", self.product_data, format="json")
        time_after_request = datetime.now(timezone.utc)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_data = response.json()["product"]

        self.assertEqual(product_data["name"], self.test_product)
        self.assertEqual(product_data["description"], self.test_description)
        self.assertEqual(product_data["price"], self.test_price)

        created_time = datetime.strptime(
            product_data["created_time"], "%Y-%m-%dT%H:%M:%S.%fZ"
        ).replace(tzinfo=timezone.utc)

        self.assertGreaterEqual(created_time, time_before_request)
        self.assertLessEqual(created_time, time_after_request)

    def test_get_products_list(self) -> None:
        self.client.post("/api/products/", self.product_data, format="json")
        response = self.client.get("/api/products/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        products = response.json()["products"]
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["name"], self.test_product)
        self.assertEqual(products[0]["description"], self.test_description)
        self.assertEqual(products[0]["price"], self.test_price)

    def test_get_product_detail(self) -> None:
        create_response = self.client.post(
            "/api/products/", self.product_data, format="json"
        )
        product_id = create_response.json()["product"]["id"]
        response = self.client.get(f"/api/products/{product_id}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = response.json()["product"]
        self.assertEqual(product_data["name"], self.test_product)
        self.assertEqual(product_data["description"], self.test_description)
        self.assertEqual(product_data["price"], self.test_price)

    def test_update_product(self) -> None:
        create_response = self.client.post(
            "/api/products/", self.product_data, format="json"
        )
        product_id = create_response.json()["product"]["id"]

        update_data = {"name": "Updated Product", "price": "39.99"}
        response = self.client.put(
            f"/api/products/{product_id}/", update_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        product_data = response.json()["product"]
        self.assertEqual(product_data["name"], "Updated Product")
        self.assertEqual(product_data["price"], "39.99")

    def test_delete_product(self) -> None:
        create_response = self.client.post(
            "/api/products/", self.product_data, format="json"
        )
        product_id = create_response.json()["product"]["id"]

        response = self.client.delete(f"/api/products/{product_id}/", format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify product is deleted
        response = self.client.get(f"/api/products/{product_id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_missing_required_fields(self) -> None:
        data = {"description": "Test Description"}
        response = self.client.post("/api/products/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        errors = response.json()["error"]
        self.assertIn("name", errors)
        self.assertIn("price", errors)
