from django.http import JsonResponse
from functools import wraps
import json
from .constants import ERROR_CODES
from rest_framework.response import Response

ACCEPTED_TOKEN = ('omni_pretest_token')

def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            return Response(
                {"message": "Unauthorized: Bearer token required", "error_code": ERROR_CODES['TOKEN_EMPTY']},
                status=400
            )

        token = auth_header[7:]

        if token not in ACCEPTED_TOKEN:
            return Response(
                {"message": "Invalid token", "error_code": ERROR_CODES['INVALID_TOKEN']},
                status=400
            )

        return view_func(request, *args, **kwargs)

    return _wrapped_view