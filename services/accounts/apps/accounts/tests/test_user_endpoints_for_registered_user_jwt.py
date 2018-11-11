from .test_user_endpoints_for_registered_user import UserEndpointsForRegisteredUserTest


class UserEndpointsForRegisteredUserAuthenticatedByJwtTest(UserEndpointsForRegisteredUserTest):
    def authenticate_tested_user(self):
        self.authenticate_tested_user_with_jwt()

    def login_and_authenticate_tested_user(self):
        self.login_and_authenticate_tested_user_with_jwt()
