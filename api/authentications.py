from django.contrib.auth.models import AnonymousUser
from rest_framework import authentication
from rest_framework import exceptions

ACCEPTED_TOKEN = ('omni_pretest_token')


class CustomUser(AnonymousUser):

    @property
    def is_authenticated(self):
        return True


class CustomAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth = authentication.get_authorization_header(request).split()

        if not auth or auth[0].lower() != b'token':
            return None

        if len(auth) == 1:
            msg = 'Invalid token header. No credentials provided.'
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = 'Invalid token header. Credentials string should not contain spaces.'
            raise exceptions.AuthenticationFailed(msg)

        if auth[1].decode("utf-8") != ACCEPTED_TOKEN:
            msg = 'Invalid token. Credentials string is not accepted.'
            raise exceptions.AuthenticationFailed(msg)
            
        return (CustomUser(), ACCEPTED_TOKEN)
