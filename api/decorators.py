from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse

ACCEPTED_TOKEN = 'omni_pretest_token'

def validate_token(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = request.headers.get('Authorization')
        if token != ACCEPTED_TOKEN:
            return JsonResponse({ "error": "Invalid or missing access token"})
        return view_func(request, *args, **kwargs)
    return _wrapped_view