from uuid import uuid4

from django.db import transaction
from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .authorization import IsOwner, add_login_permission, able_to_login, is_loggedin, \
    is_registered
from .models import User, ElevatedToken, IdentityToken
from .serializers import AuthenticatedUserSerializer, AuthorizedUserSerializer


class UserView(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer(self, *args, **kwargs):
        serializer_class = AuthorizedUserSerializer if is_loggedin(self.request) else AuthenticatedUserSerializer
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
            return [IsOwner()]
        if self.action == 'update':
            return [IsOwner()]
        if self.action == 'destroy':
            return [IsOwner()]
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
            if not able_to_login(request):
                raise PermissionDenied('No login permission!')
            if not user.check_password(request.data.get('password')):
                raise PermissionDenied('Invalid password!')
            user.date_login = timezone.now()
            elevated_token, created = ElevatedToken.objects.get_or_create(user=user)
            serializer = self.get_serializer(user, data={}, partial=True, elevated_token=elevated_token)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        # create new user otherwise
        user = User.objects.create(username='user_{}'.format(uuid4()))
        return Response(
            self.get_serializer(user, identity_token=IdentityToken.objects.get_or_create(user=user)[0]).data,
            status=status.HTTP_201_CREATED)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # register user if possible
        if all([
            not is_registered(request),
            request.data.get('username', False),
            request.data.get('email', False),
            request.data.get('password', False),
            request.data.get('accepted_privacy_policy', False),
            request.data.get('accepted_terms_of_service', False),
        ]):
            if not instance.date_registered:
                instance.date_registered = timezone.now()
            instance.is_registered = True
            instance.set_password(request.data.get('password'))
            add_login_permission(instance)
            serializer = self.get_serializer(instance, data={
                'username': request.data.get('username', instance.username),
                'email': request.data.get('email', instance.email),
                'accepted_privacy_policy': request.data.get('accepted_privacy_policy',
                                                            instance.accepted_privacy_policy),
                'accepted_terms_of_service': request.data.get('accepted_terms_of_service',
                                                              instance.accepted_terms_of_service),
            }, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow `accepted privacy_policy` field update if authenticated but not logged in and not accepted before
        if all([
            not is_registered(request),
            not instance.accepted_privacy_policy,
            request.data.get('accepted_privacy_policy', False)
        ]):
            serializer = self.get_serializer(instance,
                                             data={'accepted_privacy_policy': True},
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        # allow update if logged in
        if is_loggedin(self.request):
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise PermissionDenied()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # log out
        if is_loggedin(self.request):
            token = ElevatedToken.objects.get(user=instance)
            token.delete()
            serializer = self.get_serializer(instance, data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        raise PermissionDenied()


class UserByTokenView(UserView):
    lookup_field = None
    lookup_url_kwarg = 'token'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        assert lookup_url_kwarg in self.kwargs, (
                'Expected view %s to be called with a URL keyword argument '
                'named "%s". Fix your URL conf, or set the `.lookup_field` '
                'attribute on the view correctly.' %
                (self.__class__.__name__, lookup_url_kwarg)
        )
        try:
            user = ElevatedToken.objects.select_related('user').get(key=self.kwargs[lookup_url_kwarg]).user
        except ElevatedToken.DoesNotExist:
            try:
                user = IdentityToken.objects.select_related('user').get(key=self.kwargs[lookup_url_kwarg]).user
            except IdentityToken.DoesNotExist:
                raise Http404('No %s matches the given query.' % queryset.model._meta.object_name)
        self.check_object_permissions(self.request, user)
        return user
