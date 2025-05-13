from functools import wraps
from rest_framework.response import Response
from rest_framework import status

ACCEPTED_TOKEN = ('omni_pretest_token',)

def token_required(view_func):
    #@wraps(view_func)
    def wrapper(request, *args, **kwargs):
        access_token = request.data.get('access_token')
        
        if not access_token:
            return Response({'error': '缺少token'}, status=status.HTTP_403_FORBIDDEN)
            
        if access_token not in ACCEPTED_TOKEN:
            return Response({'error': '無效token'}, status=status.HTTP_403_FORBIDDEN)
            
        return view_func(request, *args, **kwargs)
    return wrapper
