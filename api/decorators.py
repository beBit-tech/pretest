from django.http import HttpResponseForbidden
import json

ACCEPTED_TOKEN = ("omni_pretest_token")

def api_token_required(view_func):
    def wrapper(request, *args, **kwargs):
        access_token = request.headers.get("Authorization")
        if access_token not in ACCEPTED_TOKEN:
            return HttpResponseForbidden(
                json.dumps({"Error": "Invalid Access Token"}), 
                content_type="application/json"
            )
        return view_func(request, *args, **kwargs)
    return wrapper
