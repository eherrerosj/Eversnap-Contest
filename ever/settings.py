"""
Django settings for ever project.

Author: Enrique Herreros (eherrerosj@gmail.com)
Django assignment for EverSnap. July 5th, 2014
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
from celery.schedules import crontab
import os
from datetime import timedelta
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, 'templates').replace('\\','/'),
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '+3k)d%u6...cbw'

# Turn this one to False before deployment
DEBUG = True

TEMPLATE_DEBUG = True

# Working on localhost:8000
ALLOWED_HOSTS = []


# Application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hashtag', # Our app
    'djcelery', # Django Celery for automatization
    'kombu.transport.django', # Queue for Celery
    'rest_framework', # Rest API
)

import djcelery
djcelery.setup_loader() # Load Django Celery setting
BROKER_URL = "django://" # Broker dir for queue manager

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'ever.urls'

WSGI_APPLICATION = 'ever.wsgi.application'

# Scheduler for Celery (beat). We only have the fetcher one for now
CELERYBEAT_SCHEDULE = {
    'schedule-name': { 
        'task': 'hashtag.tasks.searchpics',  # call twitter pic fetcher task
        'schedule': crontab(hour="*", minute="*/20", day_of_week="*"), # lookup every 20 mins
        'args': ("#carnival",) # always a tuple. 1st arg is the hashtag, so easy to change :)
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'), # default name for the database
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = (
    '/home/kike/eversnap/ever/static/'
)

REST_FRAMEWORK = {
    # ... only used if the `serializer_class` attribute is not set on a view.
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.HyperlinkedModelSerializer',

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}