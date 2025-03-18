# api/auth_utils.py

from functools import wraps
from rest_framework.response import Response

from .utils import parse_json_request

ACCEPTED_TOKEN = "omni_pretest_token"


def is_valid_token(token: str) -> bool:
    """
    檢查 access token 是否與預設值相同。
    """
    return token == ACCEPTED_TOKEN


def validate_access_token(view_func):
    """
    Decorator：用於驗證 access token，確保 API 只能由授權用戶存取。
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        data = parse_json_request(request)
        if not data:
            return Response({"error": "Invalid JSON format"}, status=400)

        token = data.get("access_token")
        if not is_valid_token(token):
            return Response({"error": "Invalid access token"}, status=403)

        return view_func(request, data, *args, **kwargs)

    return _wrapped_view
