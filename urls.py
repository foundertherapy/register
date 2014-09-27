from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic
import django.contrib.auth.urls
import django.conf
import django.conf.urls.static
import django.contrib.admin


urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(
        r'^$', django.views.generic.TemplateView.as_view(
            template_name='index.html')),
    django.conf.urls.url(
        r'^robots.txt$', django.views.generic.TemplateView.as_view(
            template_name='robots.txt')),
    django.conf.urls.url(
        r'^admin/', django.conf.urls.include(django.contrib.admin.site.urls)),

) + django.conf.urls.static.static(
    django.conf.settings.MEDIA_URL,
    document_root=django.conf.settings.MEDIA_ROOT)


django.contrib.admin.site.site_title = 'FiftyThree Client'
django.contrib.admin.site.site_header = 'FiftyThree Client'
django.contrib.admin.site.index_title = ''
