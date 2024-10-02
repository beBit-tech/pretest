from functools import wraps
from django.http import JsonResponse

ACCEPTED_TOKEN = ('omni_pretest_token')

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return JsonResponse({'error': 'Token is missing'}, status=401)
        if token != ACCEPTED_TOKEN:
            return JsonResponse({'error': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view
