# Github Stats Django App

A silly Github stats app built with Django.

## Running Locally

```sh
$ git clone git@github.com:itamaro/github-stats-django.git
$ cd github-stats-django

$ pipenv install

$ pipenv run python manage.py migrate
$ pipenv run python manage.py createsuperuser
$ pipenv run python manage.py collectstatic

$ pipenv run heroku local -p 8000 web
# or
$ pipenv run python manage.py runserver
```

Your app should now be running on [localhost:8000](http://localhost:8000/).

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
