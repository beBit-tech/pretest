from functools import wraps
from typing import Any, Callable

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

ACCEPTED_TOKEN = "omni_pretest_token"


def validate_token(
    view_func: Callable[[Request], Response],
) -> Callable[[Request], Response]:
    @wraps(view_func)
    def wrapper(request: Request, *args: Any, **kwargs: Any) -> Response:
        access_token = request.data.get("access_token")

        if not access_token or access_token != ACCEPTED_TOKEN:
            return Response(
                {"error": "Invalid access token"}, status=status.HTTP_401_UNAUTHORIZED
            )
        return view_func(request, *args, **kwargs)

    return wrapper
