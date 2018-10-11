from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.permissions import BasePermission

from .models import User, ElevatedToken, IdentityToken


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


def has_login_permission(instance):
    return instance.has_perm('accounts.login')


def is_authenticated(instance):
    try:
        IdentityToken.objects.select_related('user').get(user=instance)
        return True
    except IdentityToken.DoesNotExist:
        return False


def is_registered(instance):
    return instance.is_registered is True


def is_superuser(instance):
    return instance.is_superuser is True


def is_loggedin(auth):
    try:
        if auth is None:
            return False
        if isinstance(auth, ElevatedToken):
            return True
        if isinstance(auth, tuple) and isinstance(auth[1], ElevatedToken):
            return True
        return False
    except ElevatedToken.DoesNotExist:
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        try:
            # determine owner
            owner = None
            if isinstance(obj, User):
                owner = obj
            if owner is None and 'user' in obj and isinstance(obj.user, User):
                owner = obj.user
            # we cannot determine ownership, so deny access
            if owner is None:
                return False
            # inactive user cannot own anything
            if not request.user.is_active:
                return False
            # user do not own other user
            if not str(request.user.id) == str(owner.id):
                return False
            # registered user own itself only when logged in
            if request.user.is_registered:
                return is_loggedin(request.auth)
            return True
        except AttributeError:
            return False
