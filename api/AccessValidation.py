from functools import wraps
from rest_framework.response import Response
from rest_framework import status

ACCEPTED_TOKEN = 'omni_pretest_token'

def validate_token(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return Response({'error': 'Token missing'}, status=status.HTTP_400_BAD_REQUEST)

        if token != ACCEPTED_TOKEN:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return func(request, *args, **kwargs)
    
    return wrapper
