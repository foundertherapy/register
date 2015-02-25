from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic
import django.contrib.auth.urls
import django.conf
import django.conf.urls.static
import django.conf.urls.i18n


urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(
        r'^localeurl/', django.conf.urls.include('localeurl.urls')),
    django.conf.urls.url(
        r'^i18n/', django.conf.urls.include('django.conf.urls.i18n')),
    django.conf.urls.url(
        r'^robots.txt$', django.views.generic.TemplateView.as_view(
            template_name='robots.txt')),
    django.conf.urls.url(
        r'^', django.conf.urls.include('registration.urls')),
)

urlpatterns += django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT)

if django.conf.settings.DEBUG:
    import debug_toolbar
    urlpatterns += django.conf.urls.patterns('',
        django.conf.urls.url(
            r'^__debug__/', django.conf.urls.include(debug_toolbar.urls)),
    )
