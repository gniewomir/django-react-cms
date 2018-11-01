Setup
--

- to setup `.env` files run 
```shell
sudo apt-get update 
sudo apt-get install rename
find . -name "*.env.dist" -exec rename 's/.env.dist$/.env/' {} \;
```
- `docker-compose up`

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
* [x] Setup SSL for development
* [x] Rename `CMS service` to `Components service` 
* [ ] Centralized logging 
* [ ] Move JWT validation to separate, lightweight service to remove shared secret from GraphQL
* [ ] [Components service](https://github.com/gniewomir/django-react-cms/tree/master/services/cms)
* [x] [Web server](https://github.com/gniewomir/django-react-cms/tree/master/services/nginx)
* [ ] [Create React App, Storybook, Express](https://github.com/gniewomir/django-react-cms/tree/master/services/react)
* [ ] Rename project to `Enraged SOA`
* [ ] Setup Certbot for production
* [ ] Scrapper service
* [ ] Mailer service
* [ ] Media service
* [ ] Content service
* [ ] Search service 
* [ ] Automated build and pushing of images to Amazon ECR
* [ ] Automated deployment to Amazon ECS