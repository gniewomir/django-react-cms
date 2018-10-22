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
* [ ] SSR out of the box 
* [ ] Full front-end tooling out of the box
* [ ] Easy deployment and scaling 

Todo
--

* [x] [Accounts service](https://github.com/gniewomir/django-react-cms/tree/master/services/accounts)
* [ ] [GraphQL service](https://github.com/gniewomir/django-react-cms/tree/master/services/graphql)
* [ ] Rename `CMS service` to `Components service` 
* [ ] [Components service](https://github.com/gniewomir/django-react-cms/tree/master/services/cms)
* [ ] [Web server](https://github.com/gniewomir/django-react-cms/tree/master/services/nginx)
* [ ] [Create React App, Storybook, Express](https://github.com/gniewomir/django-react-cms/tree/master/services/react)
* [ ] Rename project to `Enraged SOA`
* [ ] Move JWT validation to separate, lightweight service to remove shared secret from GraphQL
* [ ] Mailer service
* [ ] Media service
* [ ] Content service
* [ ] Centralized logging 