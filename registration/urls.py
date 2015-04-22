from __future__ import unicode_literals

import django.conf.urls
import django.views.generic

import views

urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(
        r'^$', views.StateLookupView.as_view(), name='start'),
    django.conf.urls.url(
        r'^done/$', django.views.generic.TemplateView.as_view(
            template_name='formtools/wizard/done.html'),
        name='done'),
    django.conf.urls.url(
        r'^deregister-done/$', django.views.generic.TemplateView.as_view(
            template_name='registration/deregister_done.html'),
        name='deregister_done'),
    django.conf.urls.url(
        r'^restricted/$', django.views.generic.TemplateView.as_view(
            template_name='formtools/wizard/register_minor.html'),
        name='register_minor'),
    django.conf.urls.url(
        r'^reset-minor/$',
        views.ResetMinorCookieDocument.as_view(),
        name='reset_minor'),
    django.conf.urls.url(
        r'^terms-of-service/$',
        views.TermsOfServiceView.as_view(),
        name='terms_of_service'),
    django.conf.urls.url(
        r'^privacy-policy/$',
        views.PrivacyPolicyView.as_view(),
        name='privacy_policy'),
    django.conf.urls.url(
        r'^terms-of-service-by-state/$',
        views.TermsOfServiceByStateView.as_view(),
        name='terms_of_service_by_state'),
    django.conf.urls.url(
        r'^register/(?P<step>.+)/$',
        views.RegistrationWizardView.as_view(
            url_name='register', done_step_name='complete'),
        name='register'),
    django.conf.urls.url(
        r'^deregister/$',
        views.DeregistrationView.as_view(),
        name='deregister'),
    django.conf.urls.url(
        r'^not-supported/$', views.UnsupportedStateView.as_view(),
        name='unsupported_state'),
    django.conf.urls.url(
        r'^redirect/$', views.StateRedirectView.as_view(),
        name='redirect_state'),
)
