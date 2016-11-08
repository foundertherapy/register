# Django settings for 53 client project
from __future__ import unicode_literals
import os
import sys

import urlparse
import datetime
import dateutil.relativedelta

from django.utils.translation import ugettext_lazy as _


DEBUG = False

def is_environ_true(name):
    return os.environ.get(name, '').lower() in ('true', 't', '1', )


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APPSERVER = os.uname()[1]

INTERNAL_IPS = ('127.0.0.1', )
ADMINS = (
    ('Organize System', 'systems-organize@foundertherapy.co'),
)

SITE_ID = 1
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_TZ = True
APPEND_SLASH = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = os.environ.get('STATIC_URL', '/static/')
MEDIA_URL = '/media/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = urlparse.urlparse(STATIC_URL).netloc
AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True

expires = datetime.datetime.utcnow() + \
          dateutil.relativedelta.relativedelta(years=5)
expires = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
AWS_HEADERS = {
    'Expires': expires,
}

GZIP_CONTENT_TYPES = (
    'text/css',
    'application/javascript',
    'application/x-javascript',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
}

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

DATETIME_INPUT_FORMATS = (
    '%Y-%m-%d %H:%M', '%Y-%m-%d', '%Y-%m-%d %H:%M:%S',
    '%m/%d/%Y %H:%M', '%m/%d/%Y', '%m/%d/%Y %H:%M:%S',
    '%m/%d/%y %H:%M', '%m/%d/%y', '%m/%d/%y %H:%M:%S',
)

MIDDLEWARE = [
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'registration.middleware.RequestLocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.sites.middleware.CurrentSiteMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'waffle.middleware.WaffleMiddleware',
    'accountsplus.middleware.TimezoneMiddleware',
    'csp.middleware.CSPMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SECURE_BROWSER_XSS_FILTER = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
                'registration.context_processors.settings'
            ],
            'debug': DEBUG,
        }
    },
]

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

ROOT_URLCONF = 'urls'

DEBUG_TOOLBAR_PATCH_SETTINGS = False
DEBUG_TOOLBAR_CONFIG = {
    # 'SHOW_TOOLBAR_CALLBACK': 'accounts.middleware.show_toolbar',
    'RENDER_PANELS': True,
}
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    # 'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
    # 'debug_toolbar.panels.profiling.ProfilingPanel',
)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'server@organize.org')

MAILGUN_PUBLIC_API_KEY = os.environ.get('MAILGUN_PUBLIC_API_KEY')
MAILGUN_API_KEY = os.environ.get('MAILGUN_PUBLIC_API_KEY')


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admin',
    'django_extensions',
    'formtools',
    'waffle',
    'raven.contrib.django.raven_compat',
    'pipeline',
    'template_email',
    'storages',
    'bootstrap3',
    'form_utils',
    'accounts',
    'registration',
    'cobrand',
    'widget',
    'secure_redis',
    'csp',
    'axes',
    'captcha',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'accountsplus.validators.ComplexPasswordValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 9,
        }
    }, {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    }, {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
]

RAVEN_CONFIG = {
    'dsn': os.environ.get('RAVEN_DSN'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',
        'handlers': ['sentry', 'console', ],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(name)s %(processName)s %(message)s',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'null': {
            'level': 'INFO',
            'class': 'logging.NullHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false', ],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null', ],
            'propagate': True,
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', ],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console', ],
            'level': 'INFO',
            'propagate': False,
        },
        'boto': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'sentry.errors': {
            'level': 'INFO',
            'handlers': ['console', ],
            'propagate': False,
        },
    },
}

FIFTYTHREE_CLIENT_KEY = os.environ.get('FIFTYTHREE_CLIENT_KEY')
FIFTYTHREE_CLIENT_ENDPOINT = os.environ.get(
    'FIFTYTHREE_CLIENT_ENDPOINT', 'localhost:8000')
FIFTYTHREE_CLIENT_SOURCE_URL = os.environ.get(
    'FIFTYTHREE_CLIENT_SOURCE_URL', 'http://localhost')
FIFTYTHREE_CLIENT_USE_SECURE = os.environ.get(
    'FIFTYTHREE_CLIENT_USE_SECURE', '').lower() not in ('false', '0')

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', 60 * 60 * 24 * 30))
INSECURE_REDIS_DB = 0
SECURE_REDIS_DB = 1
STATIC_FILES_REDIS_DB = 2
SESSION_REDIS_DB = 3
REDIS = urlparse.urlparse(REDIS_URL)

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_REDIS_PREFIX = 'session:register'
SESSION_COOKIE_AGE = 60 * 30  # 30 minute session length
SESSION_COOKIE_NAME = 'sessionid-register'
SESSION_CACHE_ALIAS = 'session'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, SECURE_REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'REDIS_SECRET_KEY': os.getenv('REDIS_SECRET_KEY'),
            'SERIALIZER': 'secure_redis.serializer.SecureSerializer',
        },
        'KEY_PREFIX': 'register:secure',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'insecure': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, INSECURE_REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'KEY_PREFIX': 'register',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'session': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, SESSION_REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'SERIALIZER': 'secure_redis.serializer.SecureSerializer',
            'REDIS_SECRET_KEY': os.getenv('REDIS_SECRET_KEY'),
        },
        'KEY_PREFIX': SESSION_REDIS_PREFIX,
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'staticfiles': {
        'BACKEND': 'django_redis.cache.RedisCache',
        # Redis url, ensure it has correct db number - Should be the form '<host>:<port>/<db>'
        'LOCATION': "{}/{}".format(REDIS_URL, STATIC_FILES_REDIS_DB),
        'OPTIONS': {
            # "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'KEY_PREFIX': 'sf',
        'TIMEOUT': 60 * 60 * 24 * 180,  # 180 days
    },
}

DISABLE_EMAIL_VALIDATION = os.environ.get(
    'DISABLE_EMAIL_VALIDATION', '').lower() in ('true', '1')

BOOTSTRAP3 = {
    'set_placeholder': False,
    'include_jquery': True,
    'jquery_url': '//code.jquery.com/jquery-2.1.4.min.js',
    'field_renderers': {
        'default': 'registration.bootstrap3_renderers.FiftyThreeFieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },

}

EMAIL_HOST = os.environ.get('MAILGUN_SMTP_SERVER', 'localhost')
EMAIL_HOST_USER = os.environ.get('MAILGUN_SMTP_LOGIN', '')
EMAIL_HOST_PASSWORD = os.environ.get('MAILGUN_SMTP_PASSWORD', '')
EMAIL_PORT = os.environ.get('MAILGUN_SMTP_PORT', 25)
EMAIL_USE_TLS = is_environ_true('EMAIL_USE_TLS')

POSTAL_CODE_RESPONSE_CACHE_TIMEOUT = os.environ.get('POSTAL_CODE_RESPONSE_CACHE_TIMEOUT', 60 * 5)

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID', '')

AUTH_USER_MODEL = 'accounts.User'

# django-axes settings
AXES_COOLOFF_TIME = 1
AXES_LOGIN_FAILURE_LIMIT = 5
AXES_LOCKOUT_URL = 'locked/'

# captcha settings
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY')
RECAPTCHA_USE_SSL = True

LOGIN_URL = '/admin/login/'
