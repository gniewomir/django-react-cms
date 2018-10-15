from uuid import uuid4

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .authorization import IsOwner, add_login_permission, has_login_permission, is_authenticated, is_loggedin, \
    is_registered
from .models import User, ElevatedToken, IdentityToken
from .serializers import UserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if 'elevated_token' in kwargs:
            kwargs['context']['elevated_token'] = kwargs.pop('elevated_token')
        if 'identity_token' in kwargs:
            kwargs['context']['identity_token'] = kwargs.pop('identity_token')
        return serializer_class(*args, **kwargs)

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'update':
            return [IsAuthenticated(), IsOwner()]
        if self.action == 'destroy':
            return [IsAuthenticated(), IsOwner()]
        raise PermissionDenied('Unsupported action!')

    @transaction.atomic
    def create(self, request, *args, **kwargs):

        # login user if applicable
        if all([
            request.data.get('password', False),
            request.data.get('username', False) or request.data.get('email', False)
        ]):
            user = None
            if request.data.get('username', False):
                try:
                    user = User.objects.get(username=request.data.get('username'))
                except User.DoesNotExist:
                    raise PermissionDenied('Username not found!')
            if user is None and request.data.get('email', False):
                try:
                    user = User.objects.get(email=request.data.get('email'))
                except User.DoesNotExist:
                    raise PermissionDenied('Email not found!')
                except User.MultipleObjectsReturned:
                    raise PermissionDenied('Multiple emails found!')
            if not user.is_registered:
                raise PermissionDenied('Not registered!')
            if not has_login_permission(user):
                raise PermissionDenied('Login denied!')
            if not user.check_password(request.data.get('password')):
                raise PermissionDenied('Invalid password!')
            user.date_login = timezone.now()
            elevated_token, created = ElevatedToken.objects.get_or_create(user=user)
            serializer = self.get_serializer(user, data={}, partial=True, elevated_token=elevated_token)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # create new user otherwise
        user = User.objects.create(username='authenticated_{}'.format(uuid4()))
        identity_token, created = IdentityToken.objects.get_or_create(user=user)
        serializer = self.get_serializer(user,
                                         data={'username': 'authenticated_{}'.format(uuid4())}, partial=True,
                                         identity_token=identity_token)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # register user if possible
        if all([
            is_authenticated(instance),
            not is_registered(instance),
            not has_login_permission(instance),
            request.data.get('username', False),
            request.data.get('email', False),
            request.data.get('password', False),
            request.data.get('accepted_privacy_policy', False),
            request.data.get('accepted_terms_of_service', False),
        ]):
            data = {
                'username': request.data.get('username', instance.username),
                'email': request.data.get('email', instance.email),
                'accepted_privacy_policy': request.data.get('accepted_privacy_policy',
                                                            instance.accepted_privacy_policy),
                'accepted_terms_of_service': request.data.get('accepted_terms_of_service',
                                                              instance.accepted_terms_of_service),
            }
            if not instance.date_registered:
                instance.date_registered = timezone.now()
            instance.is_registered = True
            instance.set_password(request.data.get('password'))
            add_login_permission(instance)
            serializer = self.get_serializer(instance, data=data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow email and privacy_policy update if authenticated but not logged in
        if all([
            is_authenticated(instance),
            not is_loggedin(request.auth),
            request.data.get('email', False) or request.data.get('accepted_privacy_policy', False)
        ]):
            data = {'email': request.data.get('email', instance.email),
                    'accepted_privacy_policy': request.data.get('accepted_privacy_policy',
                                                                instance.accepted_privacy_policy)}
            serializer = self.get_serializer(instance,
                                             data=data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow update if registered and logged in
        if all([
            is_authenticated(instance),
            is_registered(instance),
            is_loggedin(request.auth)
        ]):
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # log out
        if all([
            is_authenticated(instance),
            is_registered(instance),
            is_loggedin(request.auth)
        ]):
            token = ElevatedToken.objects.get(user=instance)
            token.delete()
            serializer = self.get_serializer(instance, data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise PermissionDenied()
