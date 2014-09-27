from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

WSGI_APPLICATION = u'wsgi.local.application'

DEFAULT_FILE_STORAGE = u'storages.backends.overwrite.OverwriteStorage'

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASE_URL = os.environ.get(u'DATABASE_URL', u'sqlite:///fiftythree.sqlite')
DATABASES = {
    u'default': dj_database_url.parse(DATABASE_URL),
}

SECRET_KEY = '+kmou3aat2g72#5m1&jm8)&%e8+ccthb@@x8d359dj_k072azb'

print(u'Running with DEBUG={0}'.format(DEBUG))
