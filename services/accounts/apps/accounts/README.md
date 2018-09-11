Authentication/authorization flow
--

Create
-

* [ ] Receive anonymous user creation request
* [ ] Create user anonymous
* [ ] Return `authentication token`

Register
-

* [ ] Receive registration request with `authentication token`
* [ ] Find user based on `authentication token`
* [ ] Update user with data received with request
* [ ] Update user permissions with `login`, `view_own_sensitive_data`, `update_own_sensitive_data`
* [ ] Return `authentication token`

Login
-

* [ ] Receive login request with `authentication token` and login credentials
* [ ] Find user based on `authentication token`
* [ ] Check permission `login`
* [ ] Verify login credentials
* [ ] Issue and return `authorization token` giving elevated status

Logout
-
* [ ] Receive login request with `authorization token`
* [ ] Find user based on `authorization token`
* [ ] Delete `authorization token` giving elevated status
* [ ] Return `authentication token`

Provide authentication/authorization of request on behalf of anonymous user
-
* [ ] Receive request with `authentication token`
* [ ] Find user based on `authentication token`
* [ ] Return `jwt` with anonymous user permissions to authenticate SOA requests

Provide authentication/authorization of request on behalf of registered user
-

* [ ] Receive request with `authentication token`
* [ ] Find user based on `authentication token`
* [ ] Return `jwt` with registered user permissions to authenticate SOA requests

Provide authentication/authorization of request on behalf of logged in user
-

* [ ] Receive request with `authorization token`
* [ ] Find user based on `authorization token`
* [ ] Return `jwt` with logged in user permissions to authenticate SOA requests

Provide authentication/authorization of request on behalf of SOA
-

* [ ] Receive request with `soa token`
* [ ] Find user based on `soa token`
* [ ] Return `jwt` with SOA permissions to authenticate SOA requests 
