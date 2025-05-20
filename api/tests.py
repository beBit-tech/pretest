from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


class OrderTestCase(APITestCase):
    def test_import_order(self):
        client = APIClient()
        response = client.post('/api/import-order/', {
                        'token': 'invalid_token',
                        'order':{
                            'total_price': '300',
                            'product_id': 'tmptmp'
                        }
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post('/api/import-order/', {
                        'token': 'omni_pretest_token',
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/api/import-order/', {
                        'token': 'omni_pretest_token',
                        'order':{}
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/api/import-order/', {
                        'token': 'omni_pretest_token',
                        'order':{
                            'total_price': '300',
                            'product_id': 'tmptmp'
                        }
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('/api/import-order/', {
                        'token': 'omni_pretest_token',
                        'order':{
                            'order_number': 'ON20252005042422',
                            'total_price': '300',
                            'product_id': 'tmptmp'
                        }
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_import_order_advanced(self):
        client = APIClient()
        response = client.post('/api/import-order-advanced/', {
                        'order_number': 'ONONONON',
                        'total_price': '300',
                        'product_id': 'tmptmp'
                    },
                    format='json',
                    HTTP_AUTHORIZATION='Bearer unvalid_token')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post('/api/import-order-advanced/', {}, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/api/import-order-advanced/', {
                        'total_price': 300,
                        'product_id': 'tmptmp'
                    }, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('/api/import-order-advanced/', {
                        'order_number': 'ON20252005042422',
                        'total_price': 300,
                        'product_id': 'tmptmp'
                    }, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_product(self):
        client = APIClient()
        response = client.post('/api/create-product/', {
                        'type':'1',
                        'material':'2'
                    },
                    format='json',
                    HTTP_AUTHORIZATION='Bearer unvalid_token')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = client.post('/api/create-product/', {}, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = client.post('/api/create-product/', {
                        'type':'1',
                        'material':'2'
                    }, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('/api/create-product/', {
                        'id': 'abcdefgh',
                        'type':'1',
                        'material':'2'
                    }, format='json',
                    HTTP_AUTHORIZATION='Bearer omni_pretest_token')
        self.assertEqual(response.status_code, status.HTTP_200_OK)