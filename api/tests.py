from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status


# Create your tests here.
class OrderTestCase(APITestCase):
    # Add your testcase here
    def test_import_order(self):
        client = APIClient()
        response = client.post('/api/import-order/', {
                        'token': 'invalid_token',
                        'order':{
                            'total_price': '300',
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
                        }
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post('/api/import-order/', {
                        'token': 'omni_pretest_token',
                        'order':{
                            'order_number': 'ON20252005042422',
                            'total_price': '300',
                        }
                    }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
