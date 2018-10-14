from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import User

"""
Anonymous user haven't provided identity_token

Anonymous user can "create" user, to receive identity_token, allowing to become authenticated later
Anonymous user can "login" itself, to receive identity_token and elevated_token, allowing him to become authenticated or logged in later
Anonymous user cannot perform any other action
"""


class UserEndpointsForAnonymousUserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.registered_user

    def get_tested_user_password(self):
        return self.registered_user_password

    # create

    def test_create_is_allowed_without_authentication(self):
        self.assertEqual(status.HTTP_201_CREATED,
                         self.client.post(reverse('users'),
                                          format='json').status_code)

    def test_create_response_contains_identity_token(self):
        self.assertIsNotNone(self.client.post(reverse('users'),
                                              format='json').data['identity_token'])

    def test_create_user_was_created(self):
        count = User.objects.all().count()
        self.client.post(reverse('users'), format='json')
        self.assertEqual(count + 1, User.objects.all().count())

    def test_create_user_user_is_not_registered_after_creation(self):
        self.assertFalse(self.client.post(reverse('users'), format='json').data['is_registered'])

    def test_create_username_is_not_empty(self):
        self.assertTrue(bool(self.client.post(reverse('users'), format='json').data['username']))

    # create/login

    def test_login_with_email_is_allowed_without_authentication(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email,
                                           'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_email_returns_identity_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['identity_token'])

    def test_login_with_email_returns_elevated_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'email': self.get_tested_user().email, 'password': self.get_tested_user_password()},
                             format='json').data['elevated_token'])

    def test_login_with_email_fails_with_invalid_email(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': 'invalid@email.com', 'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_email_fails_with_invalid_password(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email, 'password': 'invalid_password'},
                                          format='json').status_code)

    def test_login_with_username_is_allowed_without_authentication(self):
        self.assertEqual(status.HTTP_200_OK,
                         self.client.post(reverse('users'),
                                          {'username': self.get_tested_user().username,
                                           'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_username_returns_identity_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'username': self.get_tested_user().username, 'password': self.get_tested_user_password()},
                             format='json').data['identity_token'])

    def test_login_with_username_returns_elevated_token(self):
        self.assertIsNotNone(
            self.client.post(reverse('users'),
                             {'username': self.get_tested_user().username, 'password': self.get_tested_user_password()},
                             format='json').data['elevated_token'])

    def test_login_with_username_fails_with_invalid_email(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': 'invalid_username', 'password': self.get_tested_user_password()},
                                          format='json').status_code)

    def test_login_with_username_fails_with_invalid_password(self):
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'email': self.get_tested_user().email, 'password': 'invalid_password'},
                                          format='json').status_code)

    def test_login_is_forbidden_if_user_is_not_registered(self):
        user = self.get_tested_user()
        user.is_registered = False
        user.save()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.post(reverse('users'),
                                          {'username': user.username,
                                           'password': self.get_tested_user_password()},
                                          format='json').status_code)

    # retrieve

    def test_retrieve_by_uuid_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.get(reverse('user-single', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    # update

    def test_update_by_uuid_is_forbidden_for_anonymous_user(self):
        self.assertEqual(status.HTTP_401_UNAUTHORIZED,
                         self.client.patch(reverse('user-single', args=(self.get_tested_user().id,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)
