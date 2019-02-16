release: python manage.py migrate && python manage.py collectstatic
web: gunicorn googlefit.wsgi --log-file=-
worker: celery worker -A datauploader --concurrency 1
