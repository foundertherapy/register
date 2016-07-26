from __future__ import unicode_literals

from .base import *


SSLIFY_DISABLE = True

WSGI_APPLICATION = 'wsgi.heroku.application'

import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://ubuntu@localhost:5432/circle_test')
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL)
}

SECRET_KEY = '23lq&zoojn6df5e7z#n8n$%cv9!f89c)r9!m7o8uigf2tampnf'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'DB': SECURE_REDIS_DB,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'REDIS_SECRET_KEY': 'kPEDO_pSrPh3qGJVfGAflLZXKAh4AuHU64tTlP-f_PY=',
            'CLIENT_CLASS': 'secure_redis.client.SecureDjangoRedisClient',
            'DATA_RECOVERY': {
                'OLD_KEY_PREFIX': 'register',
                'OLD_CACHE_NAME': 'insecure',
                'CLEAR_OLD_ENTRIES': False,
            }

        },
        'KEY_PREFIX': 'register:secure',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'insecure': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'DB': INSECURE_REDIS_DB,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'KEY_PREFIX': 'register',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'staticfiles': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'DB': STATIC_FILES_REDIS_DB,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'KEY_PREFIX': 'sf',
        'TIMEOUT': 60 * 60 * 24 * 180,  # 180 days
    },
}
