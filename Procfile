release: python manage.py migrate
web: gunicorn googlefit.wsgi --log-file=-
worker: celery worker -A datauploader --concurrency 1
