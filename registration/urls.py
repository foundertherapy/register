from __future__ import unicode_literals

import django.conf
import django.conf.urls
import django.views.generic

import views

urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(
        r'^$', django.views.generic.TemplateView.as_view(
            template_name='home.html'), name='home'),
    django.conf.urls.url(
        r'^start/$', views.StateLookupView.as_view(), name='start'),
    django.conf.urls.url(
        r'^register/(?P<step>.+)/$',
        views.RegistrationWizardView.as_view(
            url_name='register', done_step_name='complete'),
        name='register'),
    django.conf.urls.url(
        r'^not-supported/$', views.UnsupportedStateView.as_view(),
        name='unsupported_state'),
    django.conf.urls.url(
        r'^redirect/$', views.StateRedirectView.as_view(),
        name='redirect_state'),
)
