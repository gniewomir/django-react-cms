Authentication/authorization flow
--

* Anonymous user can `create` itself to receive `identity_token`
* Authenticated user provide aforementioned `identity_token` as request header
* Authenticated user can `update` his `accepted privacy policy` flag
* Authenticated user can provide data required for registration with `update`, to become registered user
* Registered user can provide password and username or email to receive `elevated_token`
* Logged in user provide aforementioned `elevated_token` as request header

Todo
-
* [x] Setup token authentication with login and registration
* [x] Setup ownership permissions
* [x] Setup selecting user by token, not only uuid
* [x] Setup services permissions 
* [ ] Setup JWT authentication 
* [ ] Setup changing password 
* [ ] Setup token expiration
* [ ] Choose and configure password hashing
* [ ] Gather user unique user-agent's
* [ ] Setup blocking user creation for bots
* [ ] Document accounts app endpoints 
* [ ] Create mailing service  


Todo - Bugs
-
