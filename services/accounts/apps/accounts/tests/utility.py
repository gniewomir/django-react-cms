import binascii
import os

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from rest_framework.test import APITestCase

from ..models import IdentityToken, ElevatedToken, User


class AccountsTestBase(APITestCase):
    def get_tested_user(self):
        return NotImplementedError()

    def get_tested_user_password(self):
        return NotImplementedError()

    def authenticate_tested_user(self):
        self.authenticate_user(self.get_tested_user())

    def login_and_authenticate_tested_user(self):
        self.login_user(self.get_tested_user())

    def authenticate_user(self, user):
        token = IdentityToken.objects.select_related('user').get(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def login_user(self, user):
        token, created = ElevatedToken.objects.get_or_create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def generate_random_string(self):
        return binascii.hexlify(os.urandom(20)).decode()[:20]

    def setUp(self):
        self.anonymous_user = self._get_new_anonymous_user()
        self.authenticated_user = self._get_new_authenticated_user()

        self.registered_user_email = 'registered@email.com'
        self.registered_user_password = "registered_ran123domPaWORK"
        self.registered_user_first_name = 'John'
        self.registered_user_last_name = 'Doe'
        self.registered_user = self._get_new_registered_user(self.registered_user_email, self.registered_user_password,
                                                             self.registered_user_first_name,
                                                             self.registered_user_last_name)

        self.loggedin_user_password = "loggedin_ran123domPaWORK"
        self.loggedin_user_email = 'loggedin@email.com'
        self.loggedin_user_first_name = 'Paul'
        self.loggedin_user_last_name = 'Doe'
        self.loggedin_user = self._get_new_loggedin_user(self.loggedin_user_email, self.loggedin_user_password,
                                                         self.loggedin_user_first_name, self.loggedin_user_last_name)

    def _get_and_authenticate_new_anonymous_user(self):
        user = self._get_new_anonymous_user()
        token = IdentityToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user

    def _get_and_authenticate_new_registered_user(self):
        user = self._get_new_registered_user('{}@email.com'.format(self.generate_random_string()),
                                             self.generate_random_string(),
                                             'firstName{}'.format(self.generate_random_string()),
                                             'lastName{}'.format(self.generate_random_string()))
        token = IdentityToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        return user

    def _get_and_authenticate_new_logged_in_user(self):
        user = self._get_new_registered_user('{}@email.com'.format(self.generate_random_string()),
                                             self.generate_random_string(),
                                             'firstName{}'.format(self.generate_random_string()),
                                             'lastName{}'.format(self.generate_random_string()))
        IdentityToken.objects.create(user=user)
        elevated_token = ElevatedToken.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + elevated_token.key)
        return user

    def _get_new_authenticated_user(self):
        return IdentityToken.objects.create(
            user=User.objects.create(username='test_anonymous_{}'.format(self.generate_random_string()))).user

    def _get_new_anonymous_user(self):
        return User.objects.create(username='test_anonymous_{}'.format(self.generate_random_string()))

    def _get_new_registered_user(self, email, password, first_name, last_name):
        # create login permission
        content_type = ContentType.objects.get_for_model(User)
        permission, created = Permission.objects.get_or_create(
            codename='login',
            name='Can login',
            content_type=content_type,
        )

        # register user
        user = self._get_new_authenticated_user()
        user.username = '{}{}{}'.format(first_name, last_name, self.generate_random_string())
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.accepted_privacy_policy = True
        user.accepted_terms_of_service = True
        user.is_registered = True
        user.date_registered = timezone.now()
        user.set_password(password)
        user.user_permissions.add(permission)
        user.save()
        return user

    def _get_new_loggedin_user(self, email, password, first_name, last_name):
        # login user
        user = ElevatedToken.objects.create(
            user=self._get_new_registered_user(email, password, first_name, last_name)).user
        user.date_login = timezone.now()
        user.save()
        return user
