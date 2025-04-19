from functools import wraps
from django.http import JsonResponse
from rest_framework import status
import json

ACCEPTED_TOKEN = ('omni_pretest_token')

def api_token_required(view_func):
    """
    Decorator to check API token authentication
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            token = data.get('token')
            
            if token != ACCEPTED_TOKEN:
                return JsonResponse(
                    {'error': 'Invalid access token'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return _wrapped_view 