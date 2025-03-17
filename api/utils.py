from functools import wraps

from django.http import JsonResponse
from rest_framework import status

ACCEPTED_TOKEN = ('omni_pretest_token')


def validate_token(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        token = request.headers.get("Authorization")
        if token != f"Bearer {ACCEPTED_TOKEN}":
            return JsonResponse(
                data={"message": "Unauthorized: Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return func(request, *args, **kwargs)
    return wrapper
