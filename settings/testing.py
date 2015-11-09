from __future__ import unicode_literals

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

SSLIFY_DISABLE = True

WSGI_APPLICATION = 'wsgi.heroku.application'

import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://ubuntu@localhost:5432/circle_test')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

SECRET_KEY = '23lq&zoojn6df5e7z#n8n$%cv9!f89c)r9!m7o8uigf2tampnf'
