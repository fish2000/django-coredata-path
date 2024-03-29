# Django settings for the djatacore project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = ()
MANAGERS = ADMINS

import os
virtualpath = lambda *pths: os.path.join('/Users/fish/Praxa/djatacore', *pths)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': virtualpath('var', 'db', 'dev.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '', },
    'coredata': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': virtualpath('var', 'db', 'path_coredata.db'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

CACHES = {
    'blech': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '/Users/fish/Praxa/djatacore/var/run/memcached.sock',
        'KEY_PREFIX': 'djatacore-',
    },
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ost4',
    },
}

CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = "djatacore-cache"
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

TIME_ZONE = 'America/New_York'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = False
USE_L10N = False
USE_TZ = False

DEFAULT_CHARSET = 'utf-8'

MEDIA_ROOT = virtualpath('var', 'web', 'face')
MEDIA_URL = '/face/'
TEMPLATE_DIRS = ()
STATIC_ROOT = virtualpath('var', 'web', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = ()
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'HEY NSA: FUCK YOUSE YOU FUCKIN DICKBALLS'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.core.context_processors.debug",
    #"django.core.context_processors.i18n", this is AMERICA
    "django.core.context_processors.media",
    "django.core.context_processors.static",
)

ROOT_URLCONF = 'djatacore.urls'
WSGI_APPLICATION = 'djatacore.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.markup',
    
    'south',
    'appconf',
    'tagging',
    'gunicorn',
    'signalqueue',
    'watson',
    'jangypath',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
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

SQ_QUEUES = {
    'default': {
        'ENGINE': 'signalqueue.worker.backends.DatabaseQueueProxy',
        'INTERVAL': 30, # 1/3 sec
        'OPTIONS': dict(
            app_label='signalqueue', modl_name='EnqueuedSignal'),
    },
    #'redis': {
    #    'ENGINE': 'signalqueue.worker.backends.RedisSetQueue',
    #    'INTERVAL': 30, # 1/3 sec
    #    'OPTIONS': dict(
    #        port=0, unix_socket_path="/Users/fish/Praxa/djatacore/var/run/redis.sock"),
    #},
}

SQ_RUNMODE = 'SQ_ASYNC_REQUEST'
SQ_WORKER_PORT = 11231

import platform
BASE_HOSTNAME = platform.node().lower()

