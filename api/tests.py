from datetime import datetime
import json
from venv import create
from django.test import TestCase
from rest_framework.test import APITestCase
from .models import *
from django.urls import reverse


class OrderTestCase(APITestCase):    
    # pre-contruct test data
    def setUp(self):
        self.accept_token = "omni_pretest_token"

        self.order_test = Order.objects.create(
            order_num = 21,
            total_price=1200,
            created = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        )

        self.send_data = {
            "token": self.accept_token,
            "order_num":21
        }

        self.buyuser = BuyUser.objects.create(
            name = 'test123',
            age = 23,
            email = 'test123@gmail.com'
        )

        self.seller = Seller.objects.create(
            buyeruser = self.buyuser,
            store_name = '春風小館'
        )

        self.product = Product.objects.create(
            name='保鮮膜',
            price = 29,
            stack = 40,
            descript = '便宜衛生的保鮮膜',
            seller = self.seller
        )

        self.product_sell = ProductSell.objects.create(
            product = self.product,
            order = self.order_test,
            sell_num = 20
        )

        self.comment = Comment.objects.create(
            content = '好用又便宜',
            create_time = datetime.now().strftime("%Y-%m-%d, %H:%M:%S"),
            order = self.order_test
        )
    

    def test_whether_token(self):
        '''post data 不含 token'''

        url = reverse('import-order')
        response = self.client.post(
            url,
            {
                "order_num":123
            },
            format='json'
        )

        self.assertEqual(response.status_code,400)
        self.assertIn("invalid or missing token",
            response.content.decode()
        )

    def test_not_correct_token(self):
        '''post data include incorrect token'''

        url = reverse('import-order')
        send_data = {
            "token":"not_onmi_token",
            "order_num":123
        }
        response = self.client.post(
            url,
            send_data,
            format='json'
        )

        self.assertEqual(response.status_code,400)


    def test_correct_token(self):
        '''post data include correct token'''

        url = reverse('import-order')
        send_data = {
            "token":self.accept_token,
            "order_num":21
        }
        response = self.client.post(
            url,
            send_data,
            format='json'
        )

        self.assertEqual(response.status_code,200)
        self.assertEqual(Order.objects.count(),1)  # 加入一筆資料檢查

    def test_order_detail(self):
        '''測試搜尋訂單的詳情資訊'''

        url = reverse('order_detail')
        response = self.client.post(
            url,
            self.send_data,
            format='json'
        )

        self.assertEqual(response.status_code,200)
        # self.assertEqual(Order.objects.count(),1)  # 加入一筆資料檢查

    def test_order_feedback(self):

        url = reverse('order_feedback')
        response = self.client.post(
            url,
            self.send_data,
            format='json'
        )

        self.assertEqual(response.status_code,200)
        

    def test_all_store(self):
        '''測試無參數的 GET 方法'''
        url = reverse('all_store')
        response = self.client.get(url)

        self.assertEqual(response.status_code,200)


    def test_personal_store(self):
        '''測試帶有參數的 GET 方法'''
        url = reverse('all_product_from_seller', kwargs={'seller_name':self.product.seller.buyeruser.name})
        response = self.client.get(
            url,
            format = 'json'
        )

        self.assertEqual(response.status_code,200)


        