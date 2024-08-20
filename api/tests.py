from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Customer, Order, Product


class CustomerTestAPITest(APITestCase):
    def setUp(self):
        self.url = reverse("create_customer")
        self.valid_token = "omni_pretest_token"
        self.invalid_token = "invalid_token"
        self.valid_data = {"username": "UserA", "email": "usera@example.com"}
        self.invalid_username_data = {"username": "", "email": "usera@example.com"}
        self.invalid_email_data = {"username": "UserA", "email": "email"}

    def test_create_customer_with_valid_token_and_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().username, "UserA")

    def test_create_customer_with_invild_token(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.invalid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Customer.objects.count(), 0)

    def test_create_customer_with_invild_username_data(self):
        response = self.client.post(
            self.url,
            self.invalid_username_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_with_invild_email_data(self):
        response = self.client.post(
            self.url,
            self.invalid_email_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer(self):
        self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )

        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Customer.objects.count(), 1)


class CreateProductTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("create_product")
        self.valid_token = "omni_pretest_token"
        self.invalid_token = "invalid_token"
        self.valid_data = {
            "name": "Product A",
            "price": 100,
            "quantity": 50,
        }
        self.invalid_price_data = {
            "name": "Product A",
            "price": -100,
            "quantity": 50,
        }
        self.invalid_quantity_data = {
            "name": "Product A",
            "price": 100,
            "quantity": -50,
        }

    def test_create_product_with_valid_token_and_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().name, "Product A")

    def test_create_product_with_invild_token(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.invalid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.count(), 0)

    def test_create_product_invalid_price_data(self):
        response = self.client.post(
            self.url,
            self.invalid_price_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_invalid_quantity_data(self):
        response = self.client.post(
            self.url,
            self.invalid_quantity_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicate_product(self):
        self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetProductsAPITest(APITestCase):
    def setUp(self):
        Product.objects.create(name="ProductA", price=200, quantity=10)
        Product.objects.create(name="ProductB", price=300, quantity=50)
        Product.objects.create(name="ProductC", price=500, quantity=30)
        self.url = reverse("get_products")
        self.valid_token = "omni_pretest_token"
        self.invalid_token = "invalid_token"

    def test_get_products_with_valid_token(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]["name"], "ProductA")
        self.assertEqual(response.data[1]["name"], "ProductB")
        self.assertEqual(response.data[2]["name"], "ProductC")

    def test_get_products_with_invalid_token(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=self.invalid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# Create your tests here.
class OrderTestCase(APITestCase):
    def setUp(self):
        self.url = reverse("import_order")
        self.customer = Customer.objects.create(username="user", email="user@test.com")
        self.valid_token = "omni_pretest_token"
        self.invalid_token = "invalid_token"
        self.valid_data = {
            "total_price": 1300,
            "order_number": "ORD20240820012345",
            "customer": self.customer.username
        }
        self.invalid_data = {
            "order_number": "ORD20240820012345",
            "customer": self.customer.username
        }

    def test_import_order_with_valid_token_and_data(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().order_number, "ORD20240820012345")
        self.assertEqual(Order.objects.get().total_price, 1300)

    def test_import_order_with_invalid_token(self):
        response = self.client.post(
            self.url,
            self.valid_data,
            format="json",
            HTTP_AUTHORIZATION=self.invalid_token,
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
            self.invalid_data,
            format="json",
            HTTP_AUTHORIZATION=self.valid_token,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Order.objects.count(), 0)
