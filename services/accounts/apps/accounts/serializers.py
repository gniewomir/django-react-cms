from rest_framework.serializers import ModelSerializer, SerializerMethodField, EmailField, BooleanField

from .authorization import is_loggedin, is_authenticated
from .models import User, IdentityToken, ElevatedToken


class UserSerializer(ModelSerializer):
    identity_token = SerializerMethodField(read_only=True)
    elevated_token = SerializerMethodField(read_only=True)
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

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'identity_token', 'elevated_token',
                  'is_registered', 'accepted_privacy_policy', 'accepted_terms_of_service')
        read_only_fields = ('id', 'identity_token', 'elevated_token', 'is_registered')
