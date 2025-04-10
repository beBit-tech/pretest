from django.http import JsonResponse
from functools import wraps
import json

ACCEPTED_TOKEN = ('omni_pretest_token')

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        token = json.loads(request.body).get("token",'')

        if not token:
            return JsonResponse({"error": "Unauthorized: token required"}, status=401)
        if token not in ACCEPTED_TOKEN:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view