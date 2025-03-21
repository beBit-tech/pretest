from rest_framework.test import APITestCase
from rest_framework import status

from django.utils import timezone

from .views import ACCEPTED_TOKEN
from .models import Product, Order, OrderItem
import uuid
from datetime import timedelta

# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.product = Product.objects.create(
            product_number=str(uuid.uuid4()),
            title="Test Product",
            price=50.0,
            inventory=100
        )
        self.order = Order.objects.create(
            total_price=100.0,
            status=Order.STATUS_PENDING
        )
        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            quantity=2,
            price_at_purchase=50.0,
            product_title="Test Product"
        )
        self.token = ACCEPTED_TOKEN
        self.url_import_order = "/api/import-order/"
        self.url_list_orders = "/api/list-orders/"
        self.url_delete_order = f"/api/delete-order/{self.order.order_number}/"
        self.url_get_order_by_number = f"/api/get-order-by-number/{self.order.order_number}/"
        self.url_get_order_by_product = f"/api/get-order-by-product/{self.product.product_number}/"


    def test_import_order_success(self):
        data = {
            "access_token": self.token,
            "order_items": [{
                "product_title": self.product.title,
                "quantity": 2
            }]
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertIn("order_number", response.data)
        self.assertEqual(response.data["status"], "Pending")
        self.assertEqual(response.data["total_price"], 100.0)    
        self.assertEqual(response.data["order_items"][0]["product_title"], self.product.title)
        self.assertEqual(response.data["order_items"][0]["quantity"], 2)
        self.assertEqual(response.data["order_items"][0]["price_at_purchase"], 50.0)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_import_order_invalid_token(self):
        data = {
            "access_token": "invalid_token",
            "order_items": []
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "access_token must be valid")

    def test_import_order_empty_order_items(self):
        data = {
            "access_token": self.token,
            "order_items": []
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_import_order_insufficient_inventory(self):
        data = {
            "access_token": self.token,
            "order_items": [{
                "product_title": self.product.title,
                "quantity": 101
            }]
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_order_product_not_found(self):
        data = {
            "access_token": self.token,
            "order_items": [{
                "product_title": "Invalid Product",
                "quantity": 2
            }]
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_import_order_duplicate_product(self):
        data = {
            "access_token": self.token,
            "order_items": [{
                "product_title": self.product.title,
                "quantity": 2
            }, {
                "product_title": self.product.title,
                "quantity": 3
            },]
        }
        response = self.client.post(self.url_import_order, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(response.data["error"], "Product with title already exists in the order")
        
    def test_list_orders(self):
        response = self.client.get(self.url_list_orders)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_get_order_by_number_success(self):
        response = self.client.get(self.url_get_order_by_number)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["order_number"], str(self.order.order_number))

    def test_get_order_by_number_not_found(self):
        response = self.client.get(f"/api/get-order-by-number/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_order_by_product_success(self):
        response = self.client.get(self.url_get_order_by_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_get_order_by_product_not_found(self):
        response = self.client.get(f"/api/get-order-by-product/{uuid.uuid4()}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_order_success(self):
        response = self.client.delete(self.url_delete_order)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.STATUS_FAILED)

    def test_delete_order_already_failed(self):
        self.order.status = Order.STATUS_FAILED
        self.order.save()
        response = self.client.delete(self.url_delete_order)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_order_after_one_day(self):
        self.order.created_at = timezone.now() - timedelta(days=2)
        self.order.save()
        response = self.client.delete(self.url_delete_order)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ProductTestCase(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            product_number=str(uuid.uuid4()),
            title="Test Product",
            price=50.0,
            inventory=100
        )
        self.order = Order.objects.create(
            total_price=100.0,
            status=Order.STATUS_PENDING
        )
        self.order_item = OrderItem.objects.create(
            product=self.product,
            order=self.order,
            quantity=2,
            price_at_purchase=50.0,
            product_title="Test Product"
        )
        self.url_delete_product = f"/api/delete-product/{self.product.product_number}/"

    # test product foreign key is set to null
    def test_delete_product_success(self):
        response = self.client.delete(self.url_delete_product)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.order_item.refresh_from_db()
        self.assertIsNone(self.order_item.product)