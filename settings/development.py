from __future__ import unicode_literals

from .base import *

import os

DEBUG = False
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = 'wsgi.heroku.application'

STATICFILES_STORAGE = 'storage.NonPackagingS3PipelineCachedStorage'

ADMIN_MEDIA_PREFIX = ''.join([STATIC_URL, 'admin/'])

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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
