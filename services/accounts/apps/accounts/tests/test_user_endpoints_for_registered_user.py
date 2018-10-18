from django.urls import reverse
from rest_framework import status

from .utility import AccountsTestBase
from ..models import ElevatedToken, IdentityToken

"""
Registered user provided identity_token 

Registered user can do everything what anonymous user can
Registered user cannot "retrieve" itself if not logged in
Registered user can "retrieve" itself if logged in
Registered user cannot "retrieve" other user
Registered user cannot "retrieve" other user if logged in
Registered user cannot "update" itself if not logged in
Registered user can "update" itself if logged in
Registered user if logged in can "destroy" itself to logout
"""


class UserTest(AccountsTestBase):

    def get_tested_user(self):
        return self.registered_user

    def get_tested_user_password(self):
        return self.registered_user_password

    # retrieve by uuid

    def test_retrieve_by_uuid_is_forbidden_for_registered_user_if_not_logged_in(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_user_can_retrieve_itself_if_logged_in_and_response_will_contain_elevated_token(self):
        self.login_and_authenticate_tested_user()
        self.assertIsNotNone(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                             format='json').data['elevated_token'])

    def test_retrieve_by_uuid_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_loggedin_user_cannot_retrieve_other_user(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-uuid', args=(self.loggedin_user.id,)),
                                         format='json').status_code)

    def test_retrieve_by_uuid_response_contains_service_permissions(self):
        self.login_and_authenticate_tested_user()
        service_permission = self.assign_and_return_service_permission_for_user(self.get_tested_user())
        self.assertEqual(str(service_permission),
                         self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                         format='json').data['service_permissions'][0])

    # retrieve by token

    def test_retrieve_by_token_is_forbidden_for_registered_user_if_not_logged_in(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             format='json').status_code)

    def test_retrieve_by_token_user_can_retrieve_itself_if_logged_in(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                             format='json').status_code)

    def test_retrieve_by_token_user_can_retrieve_itself_if_logged_in_and_response_will_contain_elevated_token(self):
        self.login_and_authenticate_tested_user()
        self.assertIsNotNone(
            self.client.get(reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                            format='json').data['elevated_token'])

    def test_retrieve_by_token_user_cannot_retrieve_other_user(self):
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(IdentityToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    def test_retrieve_by_token_loggedin_user_cannot_retrieve_other_user(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.get(reverse('user-single-by-token',
                                                 args=(ElevatedToken.objects.get(user=self.loggedin_user).key,)),
                                         format='json').status_code)

    def test_retrieve_by_token_response_contains_service_permissions(self):
        self.login_and_authenticate_tested_user()
        service_permission = self.assign_and_return_service_permission_for_user(self.get_tested_user())
        self.assertEqual(str(service_permission),
                         self.client.get(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             format='json').data['service_permissions'][0])

    # update by uuid

    def test_update_by_uuid_is_forbidden_for_registered_user_if_not_logged_in(self):
        new_email = 'new@email.com'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email', new_email},
                                           format='json').status_code)

    def test_update_by_uuid_is_allowed_for_registered_user_logged_in(self):
        new_email = 'new@email.com'
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': new_email},
                                           format='json').status_code)

    def test_update_by_uuid_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': user.email},
                                           format='json').status_code)

    def test_update_by_uuid_rejects_duplicated_emails(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
                                           {'email': self.loggedin_user_email, 'accepted_privacy_policy': True},
                                           format='json').status_code)

    # update by token

    def test_update_by_token_is_forbidden_for_registered_user_if_not_logged_in(self):
        new_email = 'new@email.com'
        self.authenticate_tested_user()
        self.assertEqual(status.HTTP_403_FORBIDDEN,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email', new_email},
                             format='json').status_code)

    def test_update_by_token_is_allowed_for_registered_user_logged_in(self):
        new_email = 'new@email.com'
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                             {'email': new_email},
                             format='json').status_code)

    def test_update_by_token_user_can_update_own_email_with_already_set_email(self):
        user = self.get_tested_user()
        user.email = 'test@email.com'
        user.save()
        user.refresh_from_db()
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_200_OK,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': user.email},
                             format='json').status_code)

    def test_update_by_token_rejects_duplicated_emails(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(status.HTTP_400_BAD_REQUEST,
                         self.client.patch(
                             reverse('user-single-by-token', args=(self.get_tested_user_identity_token_key(),)),
                             {'email': self.loggedin_user_email, 'accepted_privacy_policy': True},
                             format='json').status_code)

    # destroy by uuid

    def test_destroy_by_uuid_logs_user_out(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(1, ElevatedToken.objects.filter(user=self.get_tested_user()).count())
        self.client.delete(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)), format='json')
        self.assertEqual(0, ElevatedToken.objects.filter(user=self.get_tested_user()).count())

    # destroy by token

    def test_destroy_by_token_logs_user_out(self):
        self.login_and_authenticate_tested_user()
        self.assertEqual(1, ElevatedToken.objects.filter(user=self.get_tested_user()).count())
        self.client.delete(reverse('user-single-by-token', args=(self.get_tested_user_elevated_token_key(),)),
                           format='json')
        self.assertEqual(0, ElevatedToken.objects.filter(user=self.get_tested_user()).count())

    # tmp

    # def test_retrieve_by_uuid_tmp_with_jwt(self):
    #     self.login_and_authenticate_tested_user_with_jwt()
    #     from ..authorization import is_loggedin, is_authenticated
    #     print('authenticated')
    #     print(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
    #                     format='json').data)

    # print(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
    #                       format='json').data)

    # for method in self.get_tested_user_authentication_methods():
    #     getattr(self, method)()
    #     print(method)
    #     print(self.client.get(reverse('user-single-by-uuid', args=(self.get_tested_user().id,)),
    #                           format='json').data)
