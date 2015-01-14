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
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', ]

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

STATIC_ROOT = os.path.join(BASE_DIR, '.static')
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
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

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
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
    'debug_toolbar',
    'template_timings_panel',
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
    'debug_toolbar',
    'template_timings_panel',
    'bootstrap3',
    'form_utils',
)
COVERAGE_REPORT_HTML_OUTPUT_DIR = os.environ.get('CIRCLE_ARTIFACTS')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', ],
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
    },
}

FIFTYTHREE_CLIENT_KEY = os.environ.get('FIFTYTHREE_CLIENT_KEY')
FIFTYTHREE_CLIENT_ENDPOINT = os.environ.get(
    'FIFTYTHREE_CLIENT_ENDPOINT', 'localhost:8000')
FIFTYTHREE_CLIENT_SOURCE_URL = os.environ.get(
    'FIFTYTHREE_CLIENT_SOURCE_URL', 'http://localhost')
FIFTYTHREE_CLIENT_USE_SECURE = os.environ.get(
    'FIFTYTHREE_CLIENT_USE_SECURE').lower() not in ('false', '0')

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
