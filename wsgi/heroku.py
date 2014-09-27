"""
WSGI config for temp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""

import django.core.wsgi
import dj_static

application = dj_static.Cling(django.core.wsgi.get_wsgi_application())
