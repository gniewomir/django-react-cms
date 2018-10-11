from .utility import AccountsTestBase
from ..authorization import is_authenticated, is_registered, is_loggedin
from ..models import ElevatedToken, IdentityToken


class AuthorizationHelpersTest(AccountsTestBase):
    """
    User has identity_token
    """

    def test_is_authenticated(self):
        anonymous_user = self._get_new_anonymous_user()
        self.assertFalse(is_authenticated(anonymous_user))
        authenticated_user = self._get_new_authenticated_user()
        self.assertTrue(is_authenticated(authenticated_user))
        registered_user = self._get_new_registered_user('{}@e.com'.format(self.generate_random_string()),
                                                        self.generate_random_string(),
                                                        'fN{}'.format(self.generate_random_string()),
                                                        'lN{}'.format(self.generate_random_string()))
        self.assertTrue(is_authenticated(registered_user))
        loggedin_user = self._get_new_loggedin_user('{}@e.com'.format(self.generate_random_string()),
                                                    self.generate_random_string(),
                                                    'fN{}'.format(self.generate_random_string()),
                                                    'lN{}'.format(self.generate_random_string()))
        self.assertTrue(is_authenticated(loggedin_user))

    """
    User has is_registered flag set
    """

    def test_is_registered(self):
        anonymous_user = self._get_new_anonymous_user()
        self.assertFalse(is_registered(anonymous_user))
        authenticated_user = self._get_new_authenticated_user()
        self.assertFalse(is_registered(authenticated_user))
        registered_user = self._get_new_registered_user('{}@e.com'.format(self.generate_random_string()),
                                                        self.generate_random_string(),
                                                        'fN{}'.format(self.generate_random_string()),
                                                        'lN{}'.format(self.generate_random_string()))
        self.assertTrue(is_registered(registered_user))
        loggedin_user = self._get_new_loggedin_user('{}@e.com'.format(self.generate_random_string()),
                                                    self.generate_random_string(),
                                                    'fN{}'.format(self.generate_random_string()),
                                                    'lN{}'.format(self.generate_random_string()))
        self.assertTrue(is_registered(loggedin_user))

    """
    User has elevated_token
    """

    def test_is_loggedin(self):
        anonymous_user = self._get_new_anonymous_user()
        self.assertFalse(is_loggedin(None))
        authenticated_user = self._get_new_authenticated_user()
        self.assertFalse(is_loggedin(IdentityToken.objects.select_related('user').get(user=authenticated_user)))
        registered_user = self._get_new_registered_user('{}@e.com'.format(self.generate_random_string()),
                                                        self.generate_random_string(),
                                                        'fN{}'.format(self.generate_random_string()),
                                                        'lN{}'.format(self.generate_random_string()))
        self.assertFalse(is_loggedin(IdentityToken.objects.select_related('user').get(user=registered_user)))
        loggedin_user = self._get_new_loggedin_user('{}@e.com'.format(self.generate_random_string()),
                                                    self.generate_random_string(),
                                                    'fN{}'.format(self.generate_random_string()),
                                                    'lN{}'.format(self.generate_random_string()))
        self.assertTrue(is_loggedin(ElevatedToken.objects.select_related('user').get(user=loggedin_user)))
