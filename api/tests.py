from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Order, Customer, Product, OrderProduct
from rest_framework import status
from .constants import ERROR_CODES

# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.url = reverse('import_order')
        self.valid_token = 'omni_pretest_token'

        # Customer for test
        self.customer = Customer.objects.create(name="TestUser")

        # Product for test
        self.product1 = Product.objects.create(name="Laptop", price=1000)
        self.product2 = Product.objects.create(name="Mouse", price=200)

        # save customer and product uid
        self.customer_uid = self.customer.uid
        self.product1_uid = self.product1.uid
        self.product2_uid = self.product2.uid

    # Test success cases
    def test_success_import_order(self):
        data = {
            'token': self.valid_token,
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        order = Order.objects.first()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderProduct.objects.filter(order=order).count(), 2)
        self.assertEqual(Order.objects.first().customer.uid, self.customer_uid)
        self.assertEqual(Order.objects.first().total_price, 2600)

    # Test error cases
    def test_invalid_token(self):
        data = {
            'token': 'wrong_token',
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_missing_token(self):
        data = {
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_missing_customer_uid(self):
        data = {
            'token': self.valid_token,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_UID_EMPTY'])

    def test_empty_product(self):
        data = {
            'token': self.valid_token,
            'customer_uid': self.customer_uid,
            'products': []
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['PRODUCT_EMPTY'])

    def test_customer_not_exist(self):
        data = {
            'token': self.valid_token,
            'customer_uid': 'fake_customer',
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_NOT_EXIST'])

    def test_negative_product(self):
        data = {
            'token': self.valid_token,
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product2_uid,"count":-5}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_PRODUCT_COUNT'])

    def test_product_not_found(self):
        data = {
            'token': self.valid_token,
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":'fake_product',"count":3}
            ]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['PRODUCT_NOT_EXIST'])

class ProductTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.url = reverse('add_product')
        self.valid_token = 'omni_pretest_token'

    # Test success cases
    def test_success_add_product(self):
        data = {
            'token': self.valid_token,
            'name': 'laptop',
            'price': 100.00
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'laptop')

    # Test error cases
    def test_empty_product_name(self):
        data = {
            'token': self.valid_token,
            'price': 100.00
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['PRODUCT_NAME_EMPTY'])

    def test_invalid_product_price1(self):
        data = {
            'token': self.valid_token,
            'name': 'laptop',
            'price': -100
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_PRODUCT_PRICE'])

    def test_invalid_product_price2(self):
        data = {
            'token': self.valid_token,
            'name': 'laptop'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_PRODUCT_PRICE'])

class CustomerTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.url = reverse('add_customer')
        self.valid_token = 'omni_pretest_token'

    # Test success cases
    def test_success_add_product(self):
        data = {
            'token': self.valid_token,
            'name': 'Paul'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.first().name, 'Paul')

    # Test error cases
    def test_empty_customer_name(self):
        data = {
            'token': self.valid_token
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_NAME_EMPTY'])