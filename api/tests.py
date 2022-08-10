from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.conf import settings


# Create your tests here.
class OrderTestCase(APITestCase):
    '''Test for post new order'''
    def setUp(self):
        #set url for post order
        self.post_url = reverse('post-order')
        #set userA with authorization token
        self.client_a = APIClient()
        self.client_a.credentials(HTTP_AUTHORIZATION=settings.ACCEPTED_TOKEN)    
        #set userB with authorization token 
        self.client_b = APIClient()

    def test_post_order_with_token(self):
        '''with authentication token'''
        data = {'total_price':999}
        response = self.client_a.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)


    def test_post_order_without_token(self):
        '''without authentication token'''
        data = {'total_price':888}
        response = self.client_b.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_post_order_with_invalid_data(self):
        '''use invalid data'''
        data = {'total_price':"not a anumber"}
        response = self.client_a.post(self.post_url,data,format='json')
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)   