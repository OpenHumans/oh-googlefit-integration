release: python manage.py migrate
web: gunicorn googlefit.wsgi --log-file=-
worker: celery -A datauploader worker --concurrency 1
