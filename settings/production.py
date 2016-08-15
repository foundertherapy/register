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
CSRF_COOKIE_HTTPONLY = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# djangosecure settings
SECURE_FRAME_DENY = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# django csp settings
CSP_STYLE_SRC = ("'self'", STATIC_URL,
                 'https://maxcdn.bootstrapcdn.com',
                 'https://cdnjs.cloudflare.com',
                 'https://fonts.googleapis.com/css',
                 "'unsafe-inline'",
                 "'unsafe-eval'",
                 )
CSP_SCRIPT_SRC = ("'self'", STATIC_URL,
                  'https://maxcdn.bootstrapcdn.com',
                  'https://cdn.ravenjs.com',
                  'https://cdn.heapanalytics.com',
                  'https://code.jquery.com',
                  'https://www.google.com',
                  'https://cdnjs.cloudflare.com',
                  'https://www.google-analytics.com',
                  'https://www.googleadservices.com',
                  'https://connect.facebook.net',
                  'https://platform.twitter.com',
                  "'unsafe-inline'",
                  "'unsafe-eval'",
                  )
CSP_FONT_SRC = ("'self'", STATIC_URL,
                'https://maxcdn.bootstrapcdn.com',
                'https://fonts.gstatic.com',
                )
CSP_IMG_SRC = ("'self'", STATIC_URL, MEDIA_URL,
               'https://register-prod.organize.org',
               'https://secure.fastclick.net',
               'https://www.google-analytics.com',
               'https://heapanalytics.com',
               'https://www.google.com',
               'https://stats.g.doubleclick.net',
               'https://www.facebook.com',
               'https://www.googleadservices.com',
               )
CSP_MEDIA_SRC = ("'self'", MEDIA_URL, STATIC_URL, )
CSP_FRAME_SRC = ("'self'", STATIC_URL, 'https://staticxx.facebook.com', )