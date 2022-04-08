from django.test import TestCase
from rest_framework.test import APITestCase
from .models import Order,Product,ProductOrder
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import json

class OrderTestCase(APITestCase):
    def setUp(self):
        #set urls
        self.post_url = reverse('import-order')
        self.list_url = reverse('orders-list')
        #create products
        Product.objects.create(title='TV',price=36800,quantity=10)
        Product.objects.create(title='BOOK',price=288,quantity=5)
        Product.objects.create(title='PHONE',price=28900,quantity=3)
        #set a client WITH TOKEN
        self.client = APIClient()
        self.accepted_token = 'omni_pretest_token'
        self.client.credentials(HTTP_AUTHORIZATION=self.accepted_token)

    def test_get_list(self):
        response=self.client.get(self.list_url) 
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_post_order(self):
        '''Check method Post with auth/un-auth and the product quantity is correct'''
        # get products from db 
        p1=Product.objects.get(title='TV')
        p2=Product.objects.get(title='BOOK')
        p1_prev_quantity = p1.quantity
        p2_prev_quantity = p2.quantity
        data={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{p1.product_number}","quantity":1},
                {"product_number":f"{p2.product_number}","quantity":2}
            ]
        }
        response = self.client.post(self.post_url,data,format='json')
        # get new products from db 
        p1=Product.objects.get(title='TV')
        p2=Product.objects.get(title='BOOK')
        p1_new_quantity = p1.quantity
        p2_new_quantity = p2.quantity
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        #check the product quantity is correct
        self.assertEqual(p1_prev_quantity-1,p1_new_quantity)
        self.assertEqual(p2_prev_quantity-2,p2_new_quantity)
        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_post_order_with_invalid_product_number(self):
        data={
            "buyer":"Emily",
            "products_data":[
                {"product_number":"NotUUID","quantity":1},
            ]
        }
        response = self.client.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['detail'],
            f"[{{'product_number': [ErrorDetail(string='Must be a valid UUID.', code='invalid')]}}]"         
        )

    def test_post_order_with_wrong_product_number(self):
        p1=Product.objects.get(title='TV')
        not_existed_product = p1.product_number
        p1.delete()
        data={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{not_existed_product}","quantity":1},
            ]
        }
        response = self.client.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['detail'],
            f"[{{'product_number': [ErrorDetail(string='({not_existed_product}) does not exist', code='invalid')]}}]"        
        )

    def test_post_order_with_invalid_product_quantity(self):
        p1=Product.objects.get(title='TV')
        data={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{p1.product_number}","quantity":p1.quantity+1},
            ]
        }
        response = self.client.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(json.loads(response.content)['detail'],"[{'non_field_errors': [ErrorDetail(string='SORRY! The Product is out of stock', code='invalid')]}]")

    def test_put_order(self):
        '''Check method PUT with auth/un-auth and the product quantity is correct'''
        p1=Product.objects.get(title='TV')
        p2=Product.objects.get(title='BOOK')
        p1_prev_quantity = p1.quantity
        p2_prev_quantity = p2.quantity
        #Make a POST and Get the order's pk
        data_post={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{p1.product_number}","quantity":1}
            ]
        }
        response = self.client.post(self.post_url,data_post,format='json')
        pk=json.loads(response.content)['order_number']
        data_put={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{p2.product_number}","quantity":2}
            ]
        }
        response = self.client.put(reverse('orders-detail',kwargs={"pk":pk}),data_put,format='json')
        # get new products from db 
        p1=Product.objects.get(title='TV')
        p2=Product.objects.get(title='BOOK')
        p1_new_quantity = p1.quantity
        p2_new_quantity = p2.quantity
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(p1_prev_quantity,p1_new_quantity)
        self.assertEqual(p2_prev_quantity,p2_new_quantity+2)

        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.put(reverse('orders-detail',kwargs={"pk":pk}),data_put,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_delete_order(self):
        '''Check method DELETE with auth and the product quantity is correct'''
        p1=Product.objects.get(title='TV')
        p1_prev_quantity = p1.quantity
        #Make a POST and Get the order's pk
        data_post={
            "buyer":"Emily",
            "products_data":[
                {"product_number":f"{p1.product_number}","quantity":1}
            ]
        }
        response = self.client.post(self.post_url,data_post,format='json')
        pk=json.loads(response.content)['order_number']
        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.delete(reverse('orders-detail',kwargs={"pk":pk}))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        #Test for auth : add Token
        self.client.credentials(HTTP_AUTHORIZATION=self.accepted_token)
        response = self.client.delete(reverse('orders-detail',kwargs={"pk":pk}))
        # get new products from db 
        p1=Product.objects.get(title='TV')
        p1_new_quantity = p1.quantity
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(p1_prev_quantity,p1_new_quantity)

class ProductTestCase(APITestCase):
    def setUp(self):
        #set urls
        self.post_url = reverse('import-product')
        self.list_url = reverse('products-list')
        Product.objects.create(title='BOOK',price=288,quantity=5)
        #set a client WITH TOKEN
        self.client = APIClient()
        self.accepted_token = 'omni_pretest_token'
        self.client.credentials(HTTP_AUTHORIZATION=self.accepted_token)
    
    def test_get_product(self):
        response=self.client.get(self.list_url) 
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_post_product(self):
        '''Check method Post with auth/un-auth'''
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='omni_pretest_token')
        data={
            "title": "TV",
            "price": 36800,
            "quantity": "100"
        }
        response = client.post(reverse('import-product'),data,format='json')
        # get new products from db 
        self.assertTrue(Product.objects.filter(title="TV").exists())
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_put_product(self):
        #get the first item in the Model Product as pk
        pk=str(Product.objects.first().product_number)
        data={
            "title": "NEW_BOOK",
            "price": 300,
            "quantity": "100"
        }  
        response = self.client.put(reverse('products-detail',kwargs={"pk":pk}),data,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        update_product = Product.objects.get(pk=pk)
        self.assertEqual(update_product.title,"NEW_BOOK")
        self.assertEqual(update_product.price,300)
        self.assertEqual(update_product.quantity,100)
        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.put(reverse('products-detail',kwargs={"pk":pk}),data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_delete_product(self):
        #get the first item in the Model Product as pk
        pk=str(Product.objects.first().product_number)
        #Test for un-auth : remove the Token
        self.client.credentials()
        response = self.client.delete(reverse('products-detail',kwargs={"pk":pk}))
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        #Test for auth : add Token
        self.client.credentials(HTTP_AUTHORIZATION=self.accepted_token)
        response = self.client.delete(reverse('products-detail',kwargs={"pk":pk}))
        self.assertTrue(Product.DoesNotExist)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)