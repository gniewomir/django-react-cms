from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework_jwt.settings import api_settings

from .models import User, ElevatedToken, IdentityToken

jwt_decode_handler = api_settings.JWT_DECODE_HANDLER


def __add_user_permission(instance, name, codename):
    content_type = ContentType.objects.get_for_model(User)
    permission, created = Permission.objects.get_or_create(
        codename=codename,
        name=name,
        content_type=content_type,
    )
    instance.user_permissions.add(permission)
    instance.save()


def add_login_permission(instance):
    __add_user_permission(instance, 'Can login', 'login')


def able_to_login(request=None):
    return request is not None and isinstance(request.user, User) and request.user.has_perm('accounts.login')


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
    print('auth type', type(request.auth))
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
