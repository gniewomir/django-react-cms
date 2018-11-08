import os
from unittest.mock import patch

from django.test import TestCase
from rest_framework.exceptions import ValidationError
from rest_framework_jwt.utils import jwt_decode_handler, jwt_encode_handler

from ..authentication import create_service_jwt, validate_service_jwt


class AuthenticationTest(TestCase):

    def test_create_service_jwt(self):
        with patch.dict('os.environ', {'NAME': 'test'}):
            jwt = jwt_encode_handler(create_service_jwt())
            assert jwt
            payload = jwt_decode_handler(jwt)
            assert payload
            assert 'exp' in payload

    def test_create_service_jwt_fails_with_unknown_service_name(self):
        assert 'NAME' not in os.environ
        with self.assertRaises(ValidationError):
            jwt_encode_handler(create_service_jwt())

    def test_create_service_jwt_returns_correct_data(self):
        service_name = 'test'
        with patch.dict('os.environ', {'NAME': service_name}):
            payload = create_service_jwt()
            assert 'exp' in payload
            assert 'service_name' in payload
            assert payload['service_name'] == service_name
            assert 'service_permissions' in payload
            assert isinstance(payload['service_permissions'], list)
            assert payload['is_service'] is True

    def test_validate_service_jwt_token(self):
        service_name = 'test'
        with patch.dict('os.environ', {'NAME': service_name}):
            jwt = jwt_encode_handler(create_service_jwt())
            validate_service_jwt(jwt)

    def test_validate_service_jwt_fails_with_invalid_data(self):
        service_name = 'test'
        with patch.dict('os.environ', {'NAME': service_name}):
            with self.assertRaises(ValidationError):
                payload = create_service_jwt()
                payload.pop('exp')
                jwt = jwt_encode_handler(payload)
                validate_service_jwt(jwt)
            with self.assertRaises(ValidationError):
                payload = create_service_jwt()
                payload.pop('service_name')
                jwt = jwt_encode_handler(payload)
                validate_service_jwt(jwt)
            with self.assertRaises(ValidationError):
                payload = create_service_jwt()
                payload.pop('service_permissions')
                jwt = jwt_encode_handler(payload)
                validate_service_jwt(jwt)
            with self.assertRaises(ValidationError):
                payload = create_service_jwt()
                payload.pop('is_service')
                jwt = jwt_encode_handler(payload)
                validate_service_jwt(jwt)
