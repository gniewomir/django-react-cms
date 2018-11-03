Development setup
--

- to setup `.env` files run 
```shell
sudo apt-get update 
sudo apt-get install rename
find . -name "*.env.dist" -exec rename 's/.env.dist$/.env/' {} \;
```
- run `cert.sh` in nginx service to generate self signed certificate
- `docker-compose up`
- run migrations in django containers

Goals
--
* [ ] Visual page builder allowing fo quick assembling sites/pages from pre-made react components
* [ ] Fast scaffolding of new services
* [ ] React+SSR out of the box 
* [ ] Full front-end tooling out of the box
* [ ] Easy deployment and scaling 

Todo
--

* [x] [Accounts service](https://github.com/gniewomir/django-react-cms/tree/master/services/accounts)
* [x] [GraphQL service](https://github.com/gniewomir/django-react-cms/tree/master/services/graphql)
* [x] [Web server](https://github.com/gniewomir/django-react-cms/tree/master/services/nginx)
* [ ] [Create React App, Storybook, Express](https://github.com/gniewomir/django-react-cms/tree/master/services/assembler)
* [ ] [Components service](https://github.com/gniewomir/django-react-cms/tree/master/services/cms)
* [x] Setup SSL for development
* [x] Setup cleaner, properly cached, multi-stage Dockerfiles
* [x] Sort out log levels to be based on env vars, log only to stdout
* [ ] Rename project to `Enraged SOA`
* [ ] Centralized logging 

* [ ] Mailer service
* [ ] Media service
* [ ] Content service
* [ ] Search service
* [ ] Scrapper service

* [ ] Move JWT validation to separate, lightweight service to remove shared secret from GraphQL?
* [ ] Setup Certbot for production 
* [ ] Non-root processes in containers
* [ ] Setup production configuration 
* [ ] Automated build and pushing of images to Amazon ECR
* [ ] Automated deployment to Amazon ECS

Research 
--

* How to handle database migrations when deploying scaled containers without taking them all down? 