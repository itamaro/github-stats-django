# Github Stats Django App

A silly Github stats app built with Django.

## Get The Project

```sh
$ git clone git@github.com:itamaro/github-stats-django.git
$ cd github-stats-django
```

## Running Locally with Docker Compose

Assuming Docker & Docker Compose are installed:

```sh
docker-compose up
```

## Running Locally with Pipenv

Install [pipenv](https://docs.pipenv.org/) (`pip install pipenv`), and:

```sh
$ pipenv install

$ pipenv run python manage.py migrate
$ pipenv run python manage.py createsuperuser
$ pipenv run python manage.py collectstatic

$ pipenv run heroku local -p 8000 web
# or
$ pipenv run python manage.py runserver
```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## Development

Adding new external packages:

```sh
$ pipenv install cool-package
# dump packages to requirements file for Docker Compose workflow
$ pipenv run pip freeze > requirements.txt
```

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku run python manage.py createsuperuser
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)
