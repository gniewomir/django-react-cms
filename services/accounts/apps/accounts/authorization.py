from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_jwt.settings import api_settings

from .models import User, ElevatedToken, IdentityToken

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def is_authenticated(request=None):
    if request is None or not isinstance(request, Request) or not isinstance(request.user, User):
        return False
    if isinstance(request.auth, IdentityToken):
        try:
            return request.auth == IdentityToken.objects.get(user=request.user)
        except IdentityToken.DoesNotExist:
            return False
    if isinstance(request.auth, ElevatedToken):
        try:
            return request.auth == ElevatedToken.objects.get(user=request.user)
        except ElevatedToken.DoesNotExist:
            return False
    return True


def is_registered(request=None):
    return is_authenticated(request) and request.user.is_registered


def is_loggedin(request=None):
    return is_registered(request) and isinstance(request.auth, ElevatedToken)


class IsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return is_authenticated(request)


class IsOwner(BasePermission):

    def has_permission(self, request, view):
        if is_loggedin(request):
            return True
        if is_registered(request):
            return False
        return is_authenticated(request)

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, User) and obj == request.user:
            return True
        return False
