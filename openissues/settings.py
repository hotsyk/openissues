# -*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = ':memory:'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

SEND_EMAILS = False
EMAIL_HOST = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_ADDRESS_FROM = ''


if DEBUG:
    EMAIL_FAIL_SILENTLY = False
else:
    EMAIL_FAIL_SILENTLY = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'ih^s_r3qgx!8-7aj%7^tqg#mj&zpdmchbbc=+*9=y#cm&v(ga)'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

import sys
import os

PROJECT_DIR = os.path.dirname(__file__)
sys.path.append(PROJECT_DIR)
sys.path.append(PROJECT_DIR + '/apps')

MEDIA_ROOT = os.path.dirname(PROJECT_DIR)+'/static/'
MEDIA_URL = '/static/'

TEMPLATE_DIRS = (PROJECT_DIR + '/templates', )

TIME_ZONE = 'Europe/Kyiv'
LANGUAGE_CODE = 'en'

SITE_ID = 1
USE_I18N = True

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'todo.middleware.Custom403Middleware',
)
FILE_CHARSET = 'utf-8'

SESSION_SAVE_EVERY_REQUEST = False

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'context_processors.host',
    'context_processors.my_media_url',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.admin',
    'django.contrib.markup',
    'todo',
)

try:
    from local_settings import *
except ImportError:
    pass
