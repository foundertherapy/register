from __future__ import unicode_literals

import django.conf.urls
import django.views.generic

import views


urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(r'^$', views.CobrandCompanyCreateView.as_view(), name='cobrand_create', ),
    django.conf.urls.url(r'^(?P<uuid>[\w]{22})/$', views.CobrandCompanyDetailView.as_view(), name='cobrand_view'),
    django.conf.urls.url(r'^r/(?P<slug>[\w-]+)/$', views.CobrandRedirect.as_view(), name='cobrand_redirect'),
    django.conf.urls.url(
        r'^tos/$', django.views.generic.TemplateView.as_view(template_name='cobrand/tos.html'), name='cobrand_tos'),
)
