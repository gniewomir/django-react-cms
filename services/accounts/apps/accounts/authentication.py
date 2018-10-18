from rest_framework.authentication import TokenAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .models import ElevatedToken, IdentityToken


class JWTAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        return super().authenticate_credentials(payload), payload


class ElevatedTokenAuthentication(TokenAuthentication):
    def get_model(self):
        return ElevatedToken

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            return None

        if not token.user.is_active:
            return None

        return token.user, token


class IdentityTokenAuthentication(TokenAuthentication):
    def get_model(self):
        return IdentityToken
