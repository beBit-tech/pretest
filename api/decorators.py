from functools import wraps
from django.http import JsonResponse
from rest_framework import status

ACCEPTED_TOKEN = ('omni_pretest_token')

def api_token_required(view_func):
    """
    Decorator to check API token authentication from Authorization header
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            auth_header = request.headers.get('Authorization', '')
            
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                token = auth_header
            
            if not token or token != ACCEPTED_TOKEN:
                return JsonResponse(
                    {'error': 'Invalid or missing access token'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            return view_func(request, *args, **kwargs)
        except Exception as e:
            return JsonResponse(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return _wrapped_view 