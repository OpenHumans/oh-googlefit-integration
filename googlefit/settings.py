"""
Django settings for oh-googlefit-integration project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import django_heroku
import os
import logging

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG', '').lower() == 'true' else False

REMOTE = True if os.getenv('REMOTE', '').lower() == 'true' else False

ALLOWED_HOSTS = ['*']

HEROKUCONFIG_APP_NAME = os.getenv('HEROKUCONFIG_APP_NAME', '')

DEFAULT_BASE_URL = ('https://{}.herokuapp.com'.format(HEROKUCONFIG_APP_NAME) if
                    REMOTE else 'http://127.0.0.1:5000')

OPENHUMANS_APP_BASE_URL = os.getenv('APP_BASE_URL', DEFAULT_BASE_URL)
if OPENHUMANS_APP_BASE_URL[-1] == "/":
    OPENHUMANS_APP_BASE_URL = OPENHUMANS_APP_BASE_URL[:-1]

# Open Humans configuration
OPENHUMANS_LOGIN_REDIRECT_URL='/'
OPENHUMANS_CLIENT_ID = os.getenv('OPENHUMANS_CLIENT_ID')
OPENHUMANS_CLIENT_SECRET = os.getenv('OPENHUMANS_CLIENT_SECRET')
OH_ACTIVITY_PAGE = 'https://www.openhumans.org/activity/google-fit/'
OPENHUMANS_OH_BASE_URL = 'https://www.openhumans.org'

OH_API_BASE = OPENHUMANS_OH_BASE_URL + '/api/direct-sharing'
OH_DIRECT_UPLOAD = OH_API_BASE + '/project/files/upload/direct/'
OH_DIRECT_UPLOAD_COMPLETE = OH_API_BASE + '/project/files/upload/complete/'
OH_DELETE_FILES = OH_API_BASE + '/project/files/delete/'

# GoogleFit configuration
GOOGLEFIT_CLIENT_ID=os.getenv('GOOGLEFIT_CLIENT_ID')
GOOGLEFIT_CLIENT_SECRET=os.getenv('GOOGLEFIT_CLIENT_SECRET')
GOOGLEFIT_SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read',
          'https://www.googleapis.com/auth/fitness.location.read']
GOOGLEFIT_TOKEN_URI = "https://www.googleapis.com/oauth2/v3/token"

GOOGLEFIT_CLIENT_CONFIG = {"web":{"client_id": GOOGLEFIT_CLIENT_ID,
        "project_id": "logical-river-225412",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": GOOGLEFIT_TOKEN_URI,
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_secret": GOOGLEFIT_CLIENT_SECRET}
 }



REDIS_URL = os.getenv('REDIS_URL', 'redis://')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'raven.contrib.django.raven_compat',
    'openhumans',
    'datauploader',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'googlefit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'googlefit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

# Configure logging to print Django logs to the console.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class':
                'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Setry/Raven setup for error tracking

RAVEN_CONFIG = {
    'dsn': os.getenv('RAVEN_DSN'),
    'CELERY_LOGLEVEL': logging.INFO
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


django_heroku.settings(locals())
