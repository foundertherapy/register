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
CSP_STYLE_SRC = [STATIC_URL, 'https://maxcdn.bootstrapcdn.com', 'https://cdnjs.cloudflare.com', 'https://fonts.googleapis.com/css', ]
CSP_SCRIPT_SRC = [STATIC_URL, 'https://maxcdn.bootstrapcdn.com', 'https://cdn.ravenjs.com', 'sha256-R5E0hZZHI8ZgYNXkZDWjcvhS4N2NBY39iAUmpzPTYL4=',
                  'sha256-TcdixPnjQRhlAxAHYXKV+LWTnosrjPHOG3moTOQdQNQ=', 'sha256-cqN7AiVkj74EGOuHhv4EZ7lEb/jmQX69+C/rVUOqsqA=',
                  'sha256-yMGoDw7QJl/hIedAqZVCL7SuZ8ze12NayTW7A9N12OM=', 'sha256-R/d38a6707BlqMnH4uCcUEsAEMfivLq0+sNXFha3p0I=',
                  ]
CSP_FONT_SRC = [STATIC_URL, 'https://maxcdn.bootstrapcdn.com', 'https://fonts.gstatic.com',
                'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVQI12N4q6QCAAMzATQeQy8IAAAAAElFTkSuQmCC', ]
CSP_IMG_SRC = [STATIC_URL, 'https://register-dev.organize.org', 'https://secure.fastclick.net', ]
CSP_MEDIA_SRC = MEDIA_URL
