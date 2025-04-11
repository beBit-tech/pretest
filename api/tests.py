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
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
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
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')
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
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_UID_EMPTY'])

    def test_empty_product(self):
        data = {
            'customer_uid': self.customer_uid,
            'products': []
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['PRODUCT_EMPTY'])

    def test_customer_not_exist(self):
        data = {
            'customer_uid': 'fake_customer',
            'products': [
                {"uid":self.product1_uid,"count":2},
                {"uid":self.product2_uid,"count":3}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_NOT_EXIST'])

    def test_negative_product(self):
        data = {
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":self.product2_uid,"count":-5}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_PRODUCT_COUNT'])

    def test_product_not_found(self):
        data = {
            'customer_uid': self.customer_uid,
            'products': [
                {"uid":'fake_product',"count":3}
            ]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
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
            'name': 'laptop',
            'price': 100.00
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.first().name, 'laptop')

    # Test error cases
    def test_invalid_token(self):
        data = {
            'name': 'laptop',
            'price': 100.00
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_missing_token(self):
        data = {
            'name': 'laptop',
            'price': 100.00
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_empty_product_name(self):
        data = {
            'price': 100.00
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['PRODUCT_NAME_EMPTY'])

    def test_invalid_product_price1(self):
        data = {
            'name': 'laptop',
            'price': -100
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Product.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_PRODUCT_PRICE'])

    def test_invalid_product_price2(self):
        data = {
            'name': 'laptop'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
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
            'name': 'Paul'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.first().name, 'Paul')

    # Test error cases
    def test_invalid_token(self):
        data = {
            'name': 'Paul'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_missing_token(self):
        data = {
            'name': 'Paul'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_empty_customer_name(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Customer.objects.count(), 0)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_NAME_EMPTY'])

class GetOrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.customer = Customer.objects.create(name="Alice")
        self.product1 = Product.objects.create(name="Laptop", price=1000)
        self.product2 = Product.objects.create(name="Mouse", price=200)
        self.order = Order.objects.create(
            customer=self.customer,
            total_price=2600
        )
        self.op1 = OrderProduct.objects.create(
            order=self.order,
            product=self.product1,
            count=2
        )
        self.op2 = OrderProduct.objects.create(
            order=self.order,
            product=self.product2,
            count=3
        )
        self.url = reverse('get_order_detail', args=[self.order.order_number])

    # Test success cases
    def test_success_add_product(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer omni_pretest_token'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['order_number'], self.order.order_number)
        self.assertEqual(response.data['customer_uid'], self.customer.uid)
        self.assertEqual(float(response.data['total_price']), float(self.order.total_price))
        self.assertEqual(len(response.data['products']), 2)

    # Test error cases
    def test_invalid_token(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer wrong_token'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_missing_token(self):
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_order_not_exist(self):
        wrong_url = reverse('get_order_detail', args=['fake_order'])
        response = self.client.get(
            wrong_url,
            HTTP_AUTHORIZATION=f'Bearer omni_pretest_token'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['ORDER_NOT_EXIST'])

class GetCustomerOrderTestCase(APITestCase):
    # Add your testcase here
    def setUp(self):
        self.customer = Customer.objects.create(name="Alice")
        self.product1 = Product.objects.create(name="Laptop", price=1000)
        self.product2 = Product.objects.create(name="Mouse", price=200)
        self.order1 = Order.objects.create(
            customer=self.customer,
            total_price=2600
        )
        self.op1 = OrderProduct.objects.create(
            order=self.order1,
            product=self.product1,
            count=2
        )
        self.op2 = OrderProduct.objects.create(
            order=self.order1,
            product=self.product2,
            count=3
        )

        self.order2 = Order.objects.create(
            customer=self.customer,
            total_price=3800
        )
        self.op3 = OrderProduct.objects.create(
            order=self.order2,
            product=self.product1,
            count=3
        )
        self.op4 = OrderProduct.objects.create(
            order=self.order2,
            product=self.product2,
            count=4
        )
        self.url = reverse('get_customer_order', args=[self.customer.uid])

    # Test success cases
    def test_success_add_product(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer omni_pretest_token'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['customer_name'], self.customer.name)
        self.assertEqual(response.data['customer_uid'], self.customer.uid)
        self.assertEqual(len(response.data['orders']), 2)

    # Test error cases
    def test_invalid_token(self):
        response = self.client.get(
            self.url,
            HTTP_AUTHORIZATION=f'Bearer wrong_token'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_success_add_product(self):
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_order_not_exist(self):
        wrong_url = reverse('get_customer_order', args=['fake_customer'])
        response = self.client.get(
            wrong_url,
            HTTP_AUTHORIZATION=f'Bearer omni_pretest_token'
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['CUSTOMER_NOT_EXIST'])

class DeleteOrdersTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('delete_order')
        self.customer = Customer.objects.create(name="Alice")
        self.product1 = Product.objects.create(name="Laptop", price=1000)
        self.product2 = Product.objects.create(name="Mouse", price=200)
        self.order1 = Order.objects.create(
            customer=self.customer,
            total_price=2600
        )
        self.op1 = OrderProduct.objects.create(
            order=self.order1,
            product=self.product1,
            count=2
        )
        self.op2 = OrderProduct.objects.create(
            order=self.order1,
            product=self.product2,
            count=3
        )

        self.order2 = Order.objects.create(
            customer=self.customer,
            total_price=3800
        )
        self.op3 = OrderProduct.objects.create(
            order=self.order2,
            product=self.product1,
            count=3
        )
        self.op4 = OrderProduct.objects.create(
            order=self.order2,
            product=self.product2,
            count=4
        )

    def test_successful_delete(self):
        data = {
            "order_numbers": [self.order1.order_number, self.order2.order_number]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 2)
        self.assertEqual(Order.objects.count(), 0)

    def test_invalid_token(self):
        data = {
            "order_numbers": [self.order1.order_number, self.order2.order_number]
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer wrong_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_TOKEN'])

    def test_empty_token(self):
        data = {
            "order_numbers": [self.order1.order_number, self.order2.order_number]
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['TOKEN_EMPTY'])

    def test_invalid_order1(self):
        data = {
            "order_numbers": [self.order1.order_number, 'fake_order']
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 1)
        self.assertEqual(response.data['fail'], 1)
        self.assertIn('fake_order', response.data['not_found'])

    def test_invalid_order2(self):
        data = {
            "order_numbers": ['fake_order1', 'fake_order2']
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['success'], 0)
        self.assertEqual(response.data['fail'], 2)

    def test_empty_order(self):
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_ORDER'])

    def test_invalid_order_format(self):
        data = {
            "order_numbers": 'not_a_list'
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error_code'], ERROR_CODES['INVALID_ORDER'])