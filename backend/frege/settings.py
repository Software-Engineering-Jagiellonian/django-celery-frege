import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = (
    "django-insecure-18a(26fjpz)=w8kab)^gja983f#bn*g^zp#_33sv0hxb#o0aoe"
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DJANGO_DEBUG", "true").lower() == "true"

ALLOWED_HOSTS = [os.environ.get("BACKEND_HOSTNAME"), ".localhost", "127.0.0.1"]

DJANGO_CORS_ALLOWED_HOSTS = [
    os.environ.get("FRONTEND_URL", "http://localhost:4200")
]

# Application definition

PROJECT_APPS = [
    "frege",
    "frege.repositories.apps.RepositoriesConfig",
    "frege.indexers.apps.IndexersConfig",
    "frege.analyzers.apps.AnalyzersConfig",
]

EXTERNAL_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework",
    "rest_framework_api_key",
    "corsheaders",
    "django_filters",
    "channels",
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.celery',              # requires celery
    'health_check.contrib.celery_ping',         # requires celery
    'health_check.contrib.psutil',              # disk and memory utilization; requires psutil
    'health_check.contrib.redis',               # requires Redis broker
]

INSTALLED_APPS = EXTERNAL_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "frege.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "frege.wsgi.application"
ASGI_APPLICATION = "frege.asgi.application"

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# DATABASES
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DJANGO_DATABASE_NAME", "frege"),
        "USER": os.environ.get("DJANGO_DATABASE_USER", "frege"),
        "PASSWORD": os.environ.get("DJANGO_DATABASE_PASSWORD", "admin"),
        "HOST": os.environ.get("DJANGO_DATABASE_HOST", "127.0.0.1"),
        "PORT": os.environ.get("DOCKER_POSTGRES_PORT", "15432"),
    }
}

REDIS_HOST = os.environ.get("DJANGO_REDIS_HOST", "127.0.0.1")
REDIS_PORT = os.environ.get("DJANGO_REDIS_PORT", "6379")
REDIS_PERSISTENCE_ENABLED: bool = os.environ.get("REDIS_PERSISTENCE_ENABLED", "False").lower() == "true"

# CELERY STUFF
CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
# CELERY_IMPORTS = ("frege.repositories.celery_tasks",)

CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/"
CELERY_CACHE_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/"

CELERY_TASK_ROUTES = {
    "frege.repositories.tasks.process_repo_task": {"queue": "downloads"},
    "frege.repositories.tasks.crawl_repos_task": {"queue": "crawl"},
}


# CACHE

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/",
    }
}

# MISC

DOWNLOAD_PATH = os.environ.get("DJANGO_DOWNLOAD_PATH", "/var/tmp/frege/")

DOWNLOAD_DIR_MAX_SIZE_BYTES = int(
    os.environ.get("DOWNLOAD_DIR_MAX_SIZE_BYTES", "2000000000")
)

DOWNLOAD_TASK_NAME = os.environ.get(
    "DOWNLOAD_TASK_NAME", "celery@worker_downloads"
)

MAX_DOWNLOAD_TASKS_COUNT = int(
    os.environ.get("MAX_DOWNLOAD_TASKS_COUNT", "24")
)

# REST FRAMEWORK

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 100,
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend"
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "frege.utils.throttling.ApiKeyRateThrottle"
    ],
    "DEFAULT_THROTTLE_RATES": {"apikey": "500/minute"},
}


# CORS

CORS_ALLOWED_ORIGINS = [
    # set for production
    'http://localhost:3000',
    'http://localhost:3001',
    'http://localhost:3030'
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'OPTIONS'
]

CORS_ALLOW_CREDENTIALS = True

# CHANNELS

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}


# HEALTHCHECK

HEALTH_CHECK = {
    'DISK_USAGE_MAX': 70,  # percent
    'MEMORY_MIN': 100,    # in MB
}

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/"
# CELERY_BROKER_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/"
# CELERY_RESULT_BACKEND = f"redis://{REDIS_HOST}:{REDIS_PORT}/"
HEALTHCHECK_CELERY_TIMEOUT = 1
HEALTHCHECK_CELERY_PING_TIMEOUT = 1
HEALTHCHECK_CELERY_QUEUE_TIMEOUT = 1
