from __future__ import unicode_literals

from .base import *


DEBUG = False
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = 'wsgi.heroku.application'

import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(
        'postgres://ubuntu@localhost:5432/circle_test'),
}

SECRET_KEY = '23lq&zoojn6df5e7z#n8n$%cv9!f89c)r9!m7o8uigf2tampnf'
