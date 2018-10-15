from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import ElevatedToken

"""
Authenticated user provided identity_token 

Authenticated user can do everything what anonymous user can
Authenticated user can "retrieve" itself
Authenticated user cannot "retrieve" other user
Authenticated user can "update" field "email"
Authenticated user can "update" field "accepted_privacy_policy"
Authenticated user cannot "update" other user
Authenticated user can "register" itself if he will provide all required data with update request
"""


class UserEndpointsForAuthenticatedUserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.authenticated_user

    def get_tested_user_password(self):
        return None

    # retrieve

    def test_retrieve_by_uuid_user_can_retrieve_itself(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_returns_identity_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                             format='json').data['identity_token'])

    def test_retrieve_by_uuid_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    def test_retrieve_by_token_user_can_retrieve_itself(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             format='json').status_code)

    def test_retrieve_by_token_returns_identity_token(self):
        self.authenticate_tested_user()
        self.assertIsNotNone(
            self.client.get(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                            format='json').data['identity_token'])

    def test_retrieve_by_token_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    # update

    def test_update_by_uuid_user_cannot_update_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_uuid_user_can_update_own_email_and_privacy_policy(self):
        new_email = 'new@email.com'
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': new_email, 'accepted_privacy_policy': new_accepted_privacy_policy},
                                           format='json').status_code)

    def test_update_by_uuid_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': user.email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    def test_update_by_uuid_user_returns_updated_email_and_privacy_policy(self):
        new_email = 'new@email.com'
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        response = self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                     {'email': new_email, 'accepted_privacy_policy': new_accepted_privacy_policy},
                                     format='json')
        self.assertEqual(new_email, response.data['email'])
        self.assertEqual(new_accepted_privacy_policy, response.data['accepted_privacy_policy'])

    def test_update_by_uuid_rejects_duplicated_emails(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': self.registered_user_email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    def test_update_by_uuid_user_cannot_update_anything_but_email_and_privacy_policy(self):
        new_username = 'new-username'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'username': new_username},
                                           format='json').status_code)

    def test_update_by_token_user_cannot_update_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-token', args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                           {'email': 'new@email.com'},
                                           format='json').status_code)

    def test_update_by_token_user_can_update_own_email_and_privacy_policy(self):
        new_email = 'new@email.com'
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                           {'email': new_email, 'accepted_privacy_policy': new_accepted_privacy_policy},
                                           format='json').status_code)

    def test_update_by_token_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                           {'email': user.email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    def test_update_by_token_user_returns_updated_email_and_privacy_policy(self):
        new_email = 'new@email.com'
        new_accepted_privacy_policy = True
        self.authenticate_tested_user()
        response = self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                     {'email': new_email, 'accepted_privacy_policy': new_accepted_privacy_policy},
                                     format='json')
        self.assertEqual(new_email, response.data['email'])
        self.assertEqual(new_accepted_privacy_policy, response.data['accepted_privacy_policy'])

    def test_update_by_token_rejects_duplicated_emails(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                           {'email': self.registered_user_email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    def test_update_by_token_user_cannot_update_anything_but_email_and_privacy_policy(self):
        new_username = 'new-username'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                           {'username': new_username},
                                           format='json').status_code)

    # update/register

    def test_update_by_uuid_with_values_required_by_registration_sets_registered_flag(self):
        self.authenticate_tested_user()
        self.assertTrue(self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                          data={'username': 'test', 'email': 'test@test.net',
                                                'password': 'password', 'accepted_privacy_policy': True,
                                                'accepted_terms_of_service': True},
                                          format='json').data['is_registered'])

    def test_update_by_uuid_with_values_required_by_registration_adds_login_permission(self):
        self.authenticate_tested_user()
        self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                          data={'username': 'test', 'email': 'test@test.net',
                                'password': 'password', 'accepted_privacy_policy': True,
                                'accepted_terms_of_service': True},
                          format='json')
        self.get_tested_user().refresh_from_db()
        self.assertTrue(self.get_tested_user().has_perm('accounts.login'))

    def test_update_by_token_with_values_required_by_registration_sets_registered_flag(self):
        self.authenticate_tested_user()
        self.assertTrue(self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                                          data={'username': 'test', 'email': 'test@test.net',
                                                'password': 'password', 'accepted_privacy_policy': True,
                                                'accepted_terms_of_service': True},
                                          format='json').data['is_registered'])

    def test_update_by_token_with_values_required_by_registration_adds_login_permission(self):
        self.authenticate_tested_user()
        self.client.patch(reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                          data={'username': 'test', 'email': 'test@test.net',
                                'password': 'password', 'accepted_privacy_policy': True,
                                'accepted_terms_of_service': True},
                          format='json')
        self.get_tested_user().refresh_from_db()
        self.assertTrue(self.get_tested_user().has_perm('accounts.login'))