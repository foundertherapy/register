from __future__ import unicode_literals

from .base import *

import os

import dj_database_url


WSGI_APPLICATION = 'wsgi.heroku.application'

STATICFILES_STORAGE = 'storage.NonPackagingS3PipelineCachedStorage'
DEFAULT_FILE_STORAGE = 'storage.MediaStorage'
MEDIA_URL = 'https://{}/media/'.format(AWS_S3_CUSTOM_DOMAIN)

ADMIN_MEDIA_PREFIX = ''.join([STATIC_URL, 'admin/'])

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

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# djangosecure settings
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True
