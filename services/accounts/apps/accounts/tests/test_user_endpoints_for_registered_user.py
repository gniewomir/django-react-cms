from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase

"""
Registered user provided identity_token 

Registered user can do everything what anonymous user can
Registered user cannot "retrieve" itself if not logged in
Registered user can "retrieve" itself if logged in
Registered user cannot "retrieve" other user
Registered user cannot "retrieve" other user if logged in
Registered user cannot "update" itself if not logged in
Registered user can "update" itself if logged in
"""


class UserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.registered_user

    def get_tested_user_password(self):
        return self.registered_user_password

    # retrieve

    def test_retrieve_by_uuid_is_forbidden_for_registered_user_if_not_logged_in(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-single', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in_and_response_will_contain_elevated_token(self):
        self.login_and_authenticate_tested_user()
        self.assertIsNotNone(self.client.get(reverse('user-single', args=(self.get_tested_user().id,)),
                                             format='json').data['elevated_token'])

    def test_retrieve_by_uuid_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_loggedin_user_cannot_retrieve_other_user(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    # update

    def test_update_by_uuid_is_forbidden_for_registered_user_if_not_logged_in(self):
        new_email = 'new@email.com'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single', args=(self.get_tested_user().id,)),
                                           {'email', new_email},
                                           format='json').status_code)

    def test_update_by_uuid_is_allowed_for_registered_user_logged_in(self):
        new_email = 'new@email.com'
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single', args=(self.get_tested_user().id,)),
                                           {'email': new_email},
                                           format='json').status_code)
