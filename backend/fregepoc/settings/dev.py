from fregepoc.settings.base import *
import os


# DATABASES
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DJANGO_DATABASE_NAME', 'frege'),
        'USER':  os.environ.get('DJANGO_DATABASE_USER', 'frege'),
        'PASSWORD': os.environ.get('DJANGO_DATABASE_PASSWORD', 'admin'),
        'HOST': os.environ.get('DJANGO_DATABASE_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DJANGO_DATABASE_PORT', '15432'),
    }
}

# CELERY STUFF
CELERY_BROKER_URL = f"redis://{os.environ.get('DJANGO_REDIS_HOST', '127.0.0.1')}:" + \
                    f"{os.environ.get('DJANGO_REDIS_PORT', '16379')}"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

