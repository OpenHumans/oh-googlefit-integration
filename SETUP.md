# Setting up your development environment for this Fitbit to Open Humans data transfer app

> Work through this guide to get this application running on your own machine

## Setting up local environment

*Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#download-and-install):*

**macOS:**

`$ brew install heroku/brew/heroku`

**Linux:**

`$ wget -qO- https://cli-assets.heroku.com/install-ubuntu.sh | sh`

**Windows:**

[Click the link](https://devcenter.heroku.com/articles/heroku-cli#download-and-install) and choose an installer to download

*Install [RabbitMQ](http://www.rabbitmq.com):*

`$ brew install rabbitmq`
`$ brew services start rabbitmq`

To set it running on very popular Ubuntu and other Debian based systems, it will likely be started for you after you install the package, but can also start it manually with:

`$ sudo rabbitmq-server start`.

*This app runs on [Python 3](https://www.python.org/downloads/).*

install the Python package  [pipenv](http://pipenv.readthedocs.io/en/latest/): `$ pip install pipenv`

### Installing dependencies

You can install all dependencies with:

`$ pipenv install`
