from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic
import django.contrib.auth.urls
import django.conf
import django.conf.urls.static
import django.conf.urls.i18n
import django.contrib.admin


urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(r'^', django.conf.urls.include('accounts.urls')),
    django.conf.urls.url(r'^i18n/', django.conf.urls.include('django.conf.urls.i18n')),
    django.conf.urls.url(r'^robots.txt$', django.views.generic.TemplateView.as_view(template_name='robots.txt')),
    django.conf.urls.url(r'^', django.conf.urls.include('registration.urls')),
    django.conf.urls.url(r'^brand/', django.conf.urls.include('cobrand.urls')),
    django.conf.urls.url(r'^admin/', django.conf.urls.include(django.contrib.admin.site.urls)),
    django.conf.urls.url(r'^widget/', django.conf.urls.include('widget.urls')),
    django.conf.urls.url(r'^captcha/', django.conf.urls.include('captcha.urls')),
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


django.contrib.admin.site.site_title = 'Register Admin'
django.contrib.admin.site.site_header = 'Register Admin'
django.contrib.admin.site.index_title = 'Home'
django.contrib.admin.site.disable_action('delete_selected')
