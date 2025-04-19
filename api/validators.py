from decimal import Decimal
from rest_framework import status
from django.http import JsonResponse
from api.models import Order

class OrderValidator:
    """Order data validator class"""
    
    @staticmethod
    def validate(data):
        order_number = data.get('order_number')
        total_price = data.get('total_price')

        if not order_number:
            return False, JsonResponse(
                {'error': 'Order number cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if Order.objects.filter(order_number=order_number).exists():
            return False, JsonResponse(
                {'error': 'Order number already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not total_price:
            return False, JsonResponse(
                {'error': 'Total price cannot be empty'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(total_price, (int, float)):
            return False, JsonResponse(
                {'error': 'Total price must be a valid number'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if isinstance(total_price, (int, float)) and Decimal(str(total_price)) <= 0:
            return False, JsonResponse(
                {'error': 'Total price must be greater than zero'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        return True, None 