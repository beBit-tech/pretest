from django.http import HttpResponseBadRequest

ACCEPTED_TOKEN = ('omni_pretest_token')

def check_access_token(view_func):
    def _wrapped_view(request, *args, **kwargs):
        token = request.data.get('token')
        if token not in ACCEPTED_TOKEN:
            return HttpResponseBadRequest('Invalid token')
        return view_func(request, *args, **kwargs)
    return _wrapped_view