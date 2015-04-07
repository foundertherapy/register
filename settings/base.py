# Django settings for 53 client project
from __future__ import unicode_literals
import os
import sys
import urlparse
from django.utils.translation import ugettext_lazy as _


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
APPSERVER = os.uname()[1]

INTERNAL_IPS = ('127.0.0.1', )

SITE_ID = 1
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en-us'
USE_TZ = True
APPEND_SLASH = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]

# Configuration for django-storages to use S3
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_SECURE_URLS = True
AWS_REDUCED_REDUNDANCY = False
AWS_PRELOAD_METADATA = True
AWS_IS_GZIPPED = True
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True

import datetime
import dateutil.relativedelta
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

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

PIPELINE_ENABLED = True
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.CachedFileFinder',
    'pipeline.finders.PipelineFinder',
)

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

MIDDLEWARE_CLASSES = [
    'sslify.middleware.SSLifyMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

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
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
    'debug_toolbar.panels.cache.CachePanel',
    # 'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    # 'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
)

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL',
                                    'server@foundertherapy.co')

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
    'djangosecure',
    'django_coverage',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'pipeline',
    'storages',
    'bootstrap3',
    'form_utils',
    'registration',
)

COVERAGE_MODULE_EXCLUDES = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'djangosecure',
    'django_coverage',
    'django_extensions',
    'raven.contrib.django.raven_compat',
    'pipeline',
    'storages',
    'debug_toolbar',
    'template_timings_panel',
    'bootstrap3',
    'form_utils',
)
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.environ.get('CIRCLE_ARTIFACTS')

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

REDIS_URL = os.getenv('REDISCLOUD_URL', 'redis://localhost:6379')
REDIS = urlparse.urlparse(REDIS_URL)
REDIS_EXPIRE_TIME = int(os.getenv('REDIS_EXPIRE_TIME', 60 * 60 * 24 * 30))
REDIS_DB = 0

SESSION_ENGINE = 'redis_sessions.session'
SESSION_REDIS_HOST = REDIS.hostname
SESSION_REDIS_PORT = REDIS.port
SESSION_REDIS_DB = REDIS_DB
SESSION_REDIS_PASSWORD = REDIS.password
SESSION_REDIS_PREFIX = 'session:register'
SESSION_COOKIE_NAME = 'sessionid-register'
SESSION_COOKIE_AGE = 60 * 30  # 30 minute session length

CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ':'.join([unicode(REDIS.hostname), unicode(REDIS.port)]),
        'OPTIONS': {
            'DB': REDIS_DB,
            'PASSWORD': REDIS.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
           'PICKLE_VERSION': 2,
        },
        'KEY_PREFIX': 'register',
        'TIMEOUT': 60 * 60 * 24,  # 1 day
    },
    'staticfiles': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': ':'.join([unicode(REDIS.hostname), unicode(REDIS.port)]),
        'OPTIONS': {
            'DB': REDIS_DB,
            'PASSWORD': REDIS.password,
            'PARSER_CLASS': 'redis.connection.HiredisParser',
            'PICKLE_VERSION': 2,
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
    'jquery_url': '//code.jquery.com/jquery-2.1.3.min.js',
    'field_renderers': {
        'default': 'registration.bootstrap3_renderers.FiftyThreeFieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },

}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
