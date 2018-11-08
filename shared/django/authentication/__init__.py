from calendar import timegm
from datetime import datetime

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler

from ..authentication.serializers import CreateServiceJwtSerializer, ValidateServiceJwtSerializer

'''
Required settings
 
JWT_AUTH = {
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'lib.authentication.StrictJWTAuthentication',
    )
}
'''


class StrictJWTAuthentication(JSONWebTokenAuthentication):

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            raise AuthenticationFailed('No token!')
        try:
            payload = validate_service_jwt(jwt_value)
        except jwt.ExpiredSignature:
            raise AuthenticationFailed('Signature has expired.')
        except jwt.DecodeError:
            raise AuthenticationFailed('Error decoding signature.')
        except jwt.InvalidTokenError:
            raise AuthenticationFailed('Invalid token!')
        validate_service_jwt(payload)
        return self.authenticate_credentials(payload)

    def authenticate_credentials(self, payload):
        return payload


def create_service_jwt():
    payload = {}
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE
    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    serializer = CreateServiceJwtSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return serializer.data


def validate_service_jwt(jwt):
    payload = jwt_decode_handler(jwt)
    serializer = ValidateServiceJwtSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return payload
