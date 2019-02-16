release: make release 
web: gunicorn googlefit.wsgi --log-file=-
worker: celery worker -A datauploader --concurrency 1
