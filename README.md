# Open Humans Google Fit data integration

*This is a Django/Celery application which takes the user through authorization steps with Open Humans and Google Fit and and then adds their Google Fit data into their Open Humans account.*

This repo is based on the Open Humans [data demo template project](https://github.com/OpenHumans/oh-data-demo-template). It uses the Google Fit API to get your activity.

## Setup local development

```
pipenv install --three --dev
pipenv shell
docker run --name some-redis -p 6379:6379 -d redis
heroku local
```

## Testing

Run tests with 

```python -m pytest```

If you want to have breakpoints such as `import ipdb;ipdb.set_trace()` when testing, need to run the tests with:

```python -m pytest -s```

## Management scripts

To update the data of all registered users:

```python manage.py update_data```

(If doing this locally, the heroku app should be running)
