from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from functools import wraps

def VerifyToken(view_func):
    @wraps(view_func)
    def _wrapped_view(request,*args,**kwargs):
        if request.headers.get('Authorization') != settings.ACCEPTED_TOKEN:
            return Response({'error':'Unauthorized operation(token needed)'}, status=status.HTTP_401_UNAUTHORIZED)
        return view_func(request,*args,**kwargs) 
    return _wrapped_view       
