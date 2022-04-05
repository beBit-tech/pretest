from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer


class OrderTestCase(APITestCase):
    def test_get_without_token(self):
        """
        GET request without a token should 200 OK
        and list of all Order instances.
        """
        url = reverse('import-order')
        response = self.client.get(url, format='json')
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_post_without_token(self):
        """
        POST request without a token should return 403 Forbidden 
        and exception message: Authentication credentials were not provided.
        """
        url = reverse('import-order')
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Authentication credentials were not provided."})

    def test_invalid_token(self):
        """
        request with a token not ACCEPTED_TOKEN should return 403 Forbidden 
        and exception message: Invalid token. Credentials string is not accepted.
        """
        url = reverse('import-order')
        token = 'omni_pretest_tok'
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {"detail": "Invalid token. Credentials string is not accepted."})
    
    def test_import_order(self):
        """
        accepted POST request should be successfully created
        """
        url = reverse('import-order')
        token = 'omni_pretest_token'
        data = {'order_number': 123, 'total_price': 100}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Order.objects.get().order_number, 123)

    def test_import_order_without_data(self):
        """
        accepted POST request without required data value should return 400 Bad Request.
        """
        url = reverse('import-order')
        token = 'omni_pretest_token'
        data = {}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
