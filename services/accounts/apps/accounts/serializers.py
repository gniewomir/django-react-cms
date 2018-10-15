from django.contrib.auth.models import Permission
from django.utils.text import slugify
from rest_framework.serializers import ModelSerializer, SerializerMethodField, EmailField, BooleanField, ValidationError

from .authorization import is_loggedin, is_authenticated
from .models import User, IdentityToken, ElevatedToken


class UserSerializer(ModelSerializer):
    identity_token = SerializerMethodField(read_only=True)
    elevated_token = SerializerMethodField(read_only=True)
    user_permissions = SerializerMethodField(read_only=True)
    service_permissions = SerializerMethodField(read_only=True)
    accepted_terms_of_service = BooleanField()
    accepted_privacy_policy = BooleanField()
    is_registered = BooleanField()
    email = EmailField()

    def get_identity_token(self, instance):
        if 'identity_token' in self.context:
            return self.context['identity_token'].key
        if is_authenticated(instance):
            token, created = IdentityToken.objects.get_or_create(user=instance)
            return token.key
        return None

    def get_elevated_token(self, instance):
        if 'elevated_token' in self.context:
            return self.context['elevated_token'].key
        if is_loggedin(self.context['request'].auth):
            try:
                return ElevatedToken.objects.get(user=instance).key
            except ElevatedToken.DoesNotExist:
                return None
        return None

    def get_user_permissions(self, instance):
        def get_unique_permissions_list(permissions_set):
            return list(set(['{}.{}.{}'.format(slugify(perm.content_type.app_label).replace('-', '_'),
                                               slugify(perm.content_type).replace('-', '_'),
                                               slugify(perm.codename).replace('-', '_')) for perm in permissions_set]))

        if instance.is_superuser and is_loggedin(self.context['request'].auth):
            return get_unique_permissions_list(Permission.objects.all())

        return get_unique_permissions_list(
            instance.user_permissions.all() | Permission.objects.filter(group__user=instance))

    @staticmethod
    def get_service_permissions(instance):
        return [str(perm) for perm in instance.service_permissions.all()]

    def validate_email(self, value):
        if value == self.context['user'].email:
            return value
        if User.objects.filter(email=value).exists():
            raise ValidationError('Not unique email!')
        return value

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token',
            'user_permissions', 'service_permissions', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = (
            'id', 'identity_token', 'elevated_token', 'is_registered', 'user_permissions',
            'service_permissions')
