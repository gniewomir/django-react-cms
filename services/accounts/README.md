Authentication/authorization flow
--

* Anonymous user can `create` itself to receive `identity_token`
* Authenticated user provide aforementioned `identity_token` as request header
* Authenticated user can `update` his email and privacy policy flag and `retrieve` itself
* Authenticated user can provide data required for registration with `update`, to acquire login permission and become registered user
* Registered user cannot retrieve and update itself until he logs in
* Registered user can provide password and username or email to receive `elevated_token`
* Logged in user provide aforementioned `identity_token` as request header
* Logged in user can retrieve and update itself    

Todo
-

* [x] Setup token authentication with login and registration
* [x] Setup ownership permissions
* [x] Setup selecting user by token, not only uuid
* [x] Setup services permissions 
* [ ] Setup JWT authentication 
* [ ] Setup token expiration
* [ ] Choose and configure password hashing
* [ ] Gather user unique user-agent's
* [ ] Setup blocking user creation for bots
* [ ] Create mailing service  


