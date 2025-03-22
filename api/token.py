from rest_framework.response import Response
from rest_framework import status

from functools import wraps

ACCEPTED_TOKEN = ("omni_pretest_token")

def token_validation(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.headers.get("Authorization") != ACCEPTED_TOKEN:
            return Response({"error": "access_token must be valid"}, status=status.HTTP_401_UNAUTHORIZED)
        return func(request, *args, **kwargs)
    return wrapper