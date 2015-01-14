from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = u'wsgi.local.application'

DEFAULT_FILE_STORAGE = u'storages.backends.overwrite.OverwriteStorage'

MIDDLEWARE_CLASSES += (
    u'debug_toolbar.middleware.DebugToolbarMiddleware',
)

SECRET_KEY = '+kmou3aat2g72#5m1&jm8)&%e8+ccthb@@x8d359dj_k072azb'

FIFTYTHREE_CLIENT_USE_SECURE = False

print(u'Running with DEBUG={0}'.format(DEBUG))
