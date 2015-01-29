from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = u'wsgi.local.application'

DEFAULT_FILE_STORAGE = u'storages.backends.overwrite.OverwriteStorage'
PIPELINE_ENABLED = False

SESSION_COOKIE_AGE = 60

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
INSTALLED_APPS += ('debug_toolbar', 'template_timings_panel', )

SECRET_KEY = '+kmou3aat2g72#5m1&jm8)&%e8+ccthb@@x8d359dj_k072azb'

DISABLE_EMAIL_VALIDATION = True

FIFTYTHREE_CLIENT_USE_SECURE = False

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

print(u'Running with DEBUG={0}'.format(DEBUG))
