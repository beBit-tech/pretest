import json

from api.models import Order, OrderItem, Product
from api.views import ACCEPTED_TOKEN
from django.test import TestCase
from rest_framework.test import APIClient, APITestCase


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.client = APIClient()
        self.import_url = "/api/import-order/"
        self.get_url = "/api/order/ORDER-0/"
        self.valid_token = f"Bearer {ACCEPTED_TOKEN}"
        self.product = Product.objects.create(
            product_number="PROD-1",
            product_name="test_product",
            price=25.05,
            stock_quantity=10
        )
        self.data = {
            "order_number": "ORDER-1",
            "total_price": 99.99,
            "customer_name": "elaina",
            "products": [
                {
                    "product_number": "PROD-1",
                    "quantity": 2
                }
            ]
        }

    def test_import_order_success(self):
        '''
        測試成功導入訂單
        '''

        # Given, When
        response = self.client.post(
            self.import_url,
            data=json.dumps(self.data),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("successfully", response_data['message'])

        self.assertTrue(Order.objects.filter(order_number="ORDER-1").exists())
        order = Order.objects.get(order_number="ORDER-1")
        self.assertEqual(float(order.total_price), 99.99)
        self.assertEqual(order.customer_name, "elaina")

        order_item = OrderItem.objects.get(order=order)
        self.assertEqual(order_item.product.product_number, "PROD-1")
        self.assertEqual(order_item.quantity, 2)

    def test_import_order_invalid_token(self):
        '''
        測試 access token 錯誤
        '''

        # Given, When
        response = self.client.post(
            self.import_url,
            data=json.dumps(self.data),
            HTTP_AUTHORIZATION="Bearer wrong_token",
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Invalid token')

    test_missing_fields_data = [
        ({}),
        (
            {
                "total_price": 99.99,
                "customer_name": "elaina",
                "products": [
                    {
                        "product_number": "PROD-1",
                        "quantity": 2
                    }
                ]
            }
        ),
        (
            {
                "order_number": "ORDER-1",
                "customer_name": "elaina",
                "products": [
                    {
                        "product_number": "PROD-1",
                        "quantity": 2
                    }
                ]
            }
        ),
        (
            (
                {
                    "order_number": "ORDER-1",
                    "total_price": 99.99,
                    "products": [
                        {
                            "product_number": "PROD-1",
                            "quantity": 2
                        }
                    ]
                }
            ),
        ),
        (
            (
                {
                    "order_number": "ORDER-1",
                    "total_price": 99.99,
                    "customer_name": "elaina",
                    "products": []
                }
            ),
        )
    ]

    def test_import_order_missing_fields(self):
        '''
        測試缺少必要欄位時回傳錯誤
        '''

        for data in self.test_missing_fields_data:
            # Given, When
            response = self.client.post(
                self.import_url,
                data=json.dumps(data),
                HTTP_AUTHORIZATION=self.valid_token,
                content_type='application/json'
            )

            # Then
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid request data', response.content.decode('utf-8'))

    def test_import_order_product_not_found(self):
        '''
        測試當訂單中包含不存在的產品
        '''

        # Given
        data = {
            "order_number": "ORDER-2",
            "total_price": 50.55,
            "customer_name": "elaina",
            "products": [
                {
                    "product_number": "NON_EXISTING_PROD",
                    "quantity": 2
                }
            ]
        }

        # When
        response = self.client.post(
            self.import_url,
            data=json.dumps(data),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn("Product NON_EXISTING_PROD does not exist", response_data['message'])

    def test_get_order_details_success(self):
        '''
        測試成功查詢訂單資訊
        '''

        # Given
        order = Order.objects.create(
            order_number="ORDER-0",
            total_price=100.00,
            customer_name="elaina"
        )

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2
        )

        # When
        response = self.client.get(
            self.get_url,
            HTTP_AUTHORIZATION=self.valid_token
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()

        self.assertEqual(response_data["order_number"], "ORDER-0")
        self.assertEqual(float(response_data["total_price"]), 100.00)
        self.assertEqual(response_data["customer_name"], "elaina")
        self.assertEqual(response_data["status"], "pending")

        item = response_data["items"][0]
        self.assertEqual(item["product_number"], "PROD-1")
        self.assertEqual(item["product_name"], "test_product")
        self.assertEqual(item["quantity"], 2)

    def test_get_order_details_order_not_found(self):
        '''
        測試查詢不存在的訂單時返回錯誤
        '''

        # Given, When
        response = self.client.get(
            "/api/order/NON_EXISTING_ORDER/",
            HTTP_AUTHORIZATION=self.valid_token
        )

        # Then
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn("Order NON_EXISTING_ORDER does not exist", response_data['message'])


class ProductTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_or_update_url = "/api/create-or-update-product/"
        self.delete_url = "/api/delete-product/"
        self.valid_token = f"Bearer {ACCEPTED_TOKEN}"
        self.product = Product.objects.create(
            product_number="PROD-0",
            product_name="old_product",
            price=20.00,
            stock_quantity=5
        )
        self.data = {
            "product_number": "PROD-1",
            "product_name": "test_product",
            "price": 25.05,
            "stock_quantity": 10
        }

    def test_create_product_success(self):
        '''
        測試成功建立商品
        '''

        # Given, When
        response = self.client.post(
            self.create_or_update_url,
            data=json.dumps(self.data),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("Product created successfully", response_data['message'])

        self.assertTrue(Product.objects.filter(product_number="PROD-1").exists())
        product = Product.objects.get(product_number="PROD-1")
        self.assertEqual(product.product_name, "test_product")
        self.assertEqual(float(product.price), 25.05)
        self.assertEqual(int(product.stock_quantity), 10)

    def test_update_existing_product(self):
        '''
        測試更新已存在的商品
        '''

        # Given
        updated_data = {
            "product_number": "PROD-0",
            "product_name": "updated_product",
            "price": 30.00,
            "stock_quantity": 15,
            "description": "The old product is updated"
        }

        # When
        response = self.client.post(
            self.create_or_update_url,
            data=json.dumps(updated_data),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("Product updated successfully", response_data['message'])

        product = Product.objects.get(product_number="PROD-0")
        self.assertEqual(product.product_name, "updated_product")
        self.assertEqual(float(product.price), 30.00)
        self.assertEqual(int(product.stock_quantity), 15)

    def test_create_or_update_product_invalid_token(self):
        '''
        測試 access token 錯誤
        '''

        # Given, When
        response = self.client.post(
            self.create_or_update_url,
            data=json.dumps(self.data),
            HTTP_AUTHORIZATION="Bearer wrong_token",
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Invalid token')

    test_missing_fields_data = [
        ({}),
        (
            {
                "product_name": "test_product",
                "price": 25.05,
                "stock_quantity": 10
            }
        ),
        (
            {
                "product_number": "PROD-1",
                "price": 25.05,
                "stock_quantity": 10
            }
        ),
        (
            {
                "product_number": "PROD-1",
                "product_name": "test_product",
                "stock_quantity": 10
            }
        ),
        (
            {
                "product_number": "PROD-1",
                "product_name": "test_product",
                "price": 25.05
            }
        ),
    ]

    def test_create_or_update_product_missing_fields(self):
        '''
        測試缺少必要欄位時回傳錯誤
        '''

        for data in self.test_missing_fields_data:
            # Given, When
            response = self.client.post(
                self.create_or_update_url,
                data=json.dumps(data),
                HTTP_AUTHORIZATION=self.valid_token,
                content_type='application/json'
            )

            # Then
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid request data', response.content.decode('utf-8'))

    def test_delete_product_success(self):
        '''
        測試成功刪除商品
        '''

        # Given, When
        response = self.client.delete(
            self.delete_url,
            data=json.dumps({"product_number": "PROD-0"}),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertIn("successfully", response_data['message'])
        self.assertFalse(Product.objects.filter(product_number="PROD-0").exists())

    def test_delete_product_invalid_token(self):
        '''
        測試 access token 錯誤
        '''

        # Given, When
        response = self.client.delete(
            self.delete_url,
            data=json.dumps({"product_number": "PROD-0"}),
            HTTP_AUTHORIZATION="Bearer wrong_token",
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content.decode('utf-8'), 'Invalid token')

    def test_delete_product_missing_fields(self):
        '''
        測試缺少必要欄位時回傳錯誤
        '''

        response = self.client.delete(
            self.delete_url,
            data=json.dumps({}),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid request data', response.content.decode('utf-8'))

    def test_delete_product_not_found(self):
        '''
        測試當刪除一不存在的產品時返回錯誤
        '''

        # Given, When
        response = self.client.delete(
            self.delete_url,
            data=json.dumps({"product_number": "NON_EXISTING_PROD"}),
            HTTP_AUTHORIZATION=self.valid_token,
            content_type='application/json'
        )

        # Then
        self.assertEqual(response.status_code, 404)
        response_data = response.json()
        self.assertIn("Product NON_EXISTING_PROD not found", response_data['message'])
