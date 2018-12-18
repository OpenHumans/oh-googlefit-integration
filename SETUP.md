# Setting up your development environment for this Google Fit to Open Humans data transfer app

> Work through this guide to get this application running on your own machine

## Setting up local environment

*Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install):*

**macOS:**

`$ brew install heroku/brew/heroku`

**Linux:**

`$ wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh`

**Windows:**

[Click the link](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and choose an installer to download

*Install [Redis](for the celery backend):*

Can either install it and start it up manually or run it via docker via:
```docker run --name some-redis -p 6379:6379 -d redis```

*This app runs on [Python 3](https://www.python.org/downloads/).*

install the Python package  [pipenv](http://pipenv.readthedocs.io/en/latest/): `$ pip install pipenv`

### Installing dependencies

You can install all dependencies with:

`$ pipenv install`
