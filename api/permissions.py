from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

def AcceptedToken(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.headers.get("Authorization") != settings.ACCEPTED_TOKEN:
            return Response({"detail": "Unauthorized (token required)"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return view_func(request, *args, **kwargs)

    return _wrapped_view