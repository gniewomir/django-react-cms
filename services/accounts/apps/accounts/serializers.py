from django.contrib.auth.models import Permission
from django.utils.text import slugify
from rest_framework.serializers import ModelSerializer, SerializerMethodField, EmailField, BooleanField, ValidationError
from rest_framework_jwt.settings import api_settings

from .authorization import is_loggedin
from .models import User, IdentityToken, ElevatedToken


class UserSerializer(ModelSerializer):
    identity_token = SerializerMethodField(read_only=True)
    elevated_token = SerializerMethodField(read_only=True)
    jwt_token = SerializerMethodField(read_only=True)
    user_permissions = SerializerMethodField(read_only=True)
    service_permissions = SerializerMethodField(read_only=True)
    accepted_terms_of_service = BooleanField()
    accepted_privacy_policy = BooleanField()
    is_registered = BooleanField()
    email = EmailField()

    def get_identity_token(self, instance):
        if 'identity_token' in self.context:
            return self.context['identity_token'].key
        token, created = IdentityToken.objects.get_or_create(user=instance)
        return token.key

    def get_elevated_token(self, instance):
        if 'elevated_token' in self.context:
            return self.context['elevated_token'].key
        if is_loggedin(self.context['request']):
            try:
                return ElevatedToken.objects.get(user=instance).key
            except ElevatedToken.DoesNotExist:
                return None
        return None

    def get_jwt_token(self, instance):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        return jwt_encode_handler(jwt_payload_handler(instance))

    def get_user_permissions(self, instance):
        def get_unique_permissions_list(permissions_set):
            return list(set(['{}.{}.{}'.format(slugify(perm.content_type.app_label).replace('-', '_'),
                                               slugify(perm.content_type).replace('-', '_'),
                                               slugify(perm.codename).replace('-', '_')) for perm in permissions_set]))

        if instance.is_superuser and is_loggedin(self.context['request']):
            return get_unique_permissions_list(Permission.objects.all())

        return get_unique_permissions_list(
            instance.user_permissions.all() | Permission.objects.filter(group__user=instance))

    @staticmethod
    def get_service_permissions(instance):
        return [str(perm) for perm in instance.service_permissions.all()]

    def validate_email(self, value):
        if value == self.context['request'].user.email:
            return value
        if User.objects.filter(email=value).exists():
            raise ValidationError('Not unique email!')
        return value

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token', 'jwt_token',
            'user_permissions', 'service_permissions', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = (
            'id', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'user_permissions',
            'service_permissions')


class AuthenticatedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'accepted_privacy_policy')
        read_only_fields = (
            'identity_token', 'elevated_token', 'jwt_token', 'is_registered')


class AuthorizedUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token', 'jwt_token',
            'user_permissions', 'service_permissions', 'is_registered', 'accepted_privacy_policy',
            'accepted_terms_of_service')
        read_only_fields = (
            'id', 'identity_token', 'elevated_token', 'jwt_token', 'is_registered', 'user_permissions',
            'service_permissions')
