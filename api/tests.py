from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Order, Product, OrderProduct
import json

class OrderTestCase(APITestCase):
    def setUp(self):
        # Create some product objects for testing
        self.product1 = Product.objects.create(
            product_number=1,
            name="product1",
            price=50.00,
            amount=10,
            status='available'
        )
        self.product2 = Product.objects.create(
            product_number=2,
            name="product2",
            price=100.00,
            amount=20,
            status='available'
        )

    def test_import_order_invalid_token(self):
        url = reverse('import_order')
        data = {
            'order_number': '12345',
            'payment_method': 'cash_on_delivery',
            'products': [
                {
                    'product_number': self.product1.product_number,
                    'quantity': 2
                },
                {
                    'product_number': self.product2.product_number,
                    'quantity': 1
                }
            ]
        }
        response = self.client.post(url, data, 'json', HTTP_AUTHORIZATION='invalid_token')
        self.assertEqual(response.status_code, 400)

    def test_import_order_insufficient_quantity(self):
        url = reverse('import_order')
        data = {
            'order_number': 12345,
            'payment_method': 'cash_on_delivery',
            'products': [
                {
                    'product_number': self.product1.product_number,
                    'quantity': self.product1.amount + 1  # request more than the available amount
                },
            ]
        }
        response = self.client.post(url, data, 'json', HTTP_AUTHORIZATION='omni_pretest_token')

         # expect a 400 response when quantity is insufficient
        self.assertEqual(response.status_code, 400)

    def test_import_order_exact_quantity(self):
        url = reverse('import_order')
        data = {
            'order_number': 12345,
            'payment_method': 'cash_on_delivery',
            'products': [
                {
                    'product_number': self.product1.product_number,
                    'quantity': self.product1.amount  # request exactly the available amount
                },
            ]
        }
        response = self.client.post(url, data, 'json', HTTP_AUTHORIZATION='omni_pretest_token')

        # expect a 200 response when quantity is exactly the amount
        self.assertEqual(response.status_code, 200)

        # Reload the product1 from the database
        self.product1.refresh_from_db()

        # Check if the product status has been set to 'out_of_stock'
        self.assertEqual(self.product1.status, 'out_of_stock')

    def test_import_order(self):
        url = reverse('import_order')
        data = {
            'order_number': 12345,
            'payment_method': 'cash_on_delivery',
            'products': [
                {
                    'product_number': self.product1.product_number,
                    'quantity': 2
                },
                {
                    'product_number': self.product2.product_number,
                    'quantity': 1
                }
            ]
        }
        response = self.client.post(url, data, 'json', HTTP_AUTHORIZATION='omni_pretest_token')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().order_number, 12345)

        # Check if the order's total price is calculated correctly
        order = Order.objects.get()
        self.assertEqual(order.total_price, 2 * self.product1.price + 1 * self.product2.price)

        # Check if the order has the correct products with the correct quantities
        order_product1 = OrderProduct.objects.get(order=order, product=self.product1)
        order_product2 = OrderProduct.objects.get(order=order, product=self.product2)
        self.assertEqual(order_product1.quantity, 2)
        self.assertEqual(order_product2.quantity, 1)