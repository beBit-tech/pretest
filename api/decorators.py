from django.http import JsonResponse
import functools

ACCEPTED_TOKEN = "omni_pretest_token"

def require_token(view_func):
    @functools.wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token.split(" ")[1] != ACCEPTED_TOKEN:
            return JsonResponse({"error": "Unauthorized"}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper
