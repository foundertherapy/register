from __future__ import unicode_literals

from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = 'wsgi.heroku.application'

DEFAULT_FILE_STORAGE = 'common.S3MediaStorage'
STATICFILES_STORAGE = 'common.S3StaticStorage'

import dj_database_url
DATABASE_URL = os.environ['DATABASE_URL']
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL),
}
DATABASES['default']['CONN_MAX_AGE'] = None

SECRET_KEY = os.environ['SECRET_KEY']

CONFIGURED_ALLOWED_HOSTS = os.environ['ALLOWED_HOSTS'].split(',')
for host in CONFIGURED_ALLOWED_HOSTS:
    if host:
        ALLOWED_HOSTS.append(host)

EMAIL_USE_TLS = True
EMAIL_HOST = os.environ['MAILGUN_SMTP_SERVER']
EMAIL_HOST_USER = os.environ['MAILGUN_SMTP_LOGIN']
EMAIL_HOST_PASSWORD = os.environ['MAILGUN_SMTP_PASSWORD']
EMAIL_PORT = os.environ['MAILGUN_SMTP_PORT']
