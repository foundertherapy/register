from __future__ import unicode_literals

import django.conf.urls
import django.views.generic

import views

urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(r'^$', views.StateLookupView.as_view(), name='start'),
    django.conf.urls.url(r'^update/$', views.StateLookupView.as_view(), kwargs={'update': True, }, name='update'),
    django.conf.urls.url(r'^done/$', django.views.generic.TemplateView.as_view(
        template_name='registration/done.html'), name='done'),
    django.conf.urls.url(r'^update-done/$', django.views.generic.TemplateView.as_view(
        template_name='registration/update_done.html'), name='update_done'),
    django.conf.urls.url(r'^restricted/$', django.views.generic.TemplateView.as_view(
        template_name='registration/register_minor.html'), name='register_minor'),
    django.conf.urls.url(r'^update-revoke/$', django.views.generic.TemplateView.as_view(
        template_name='registration/update_choice.html'), name='update_choice'),
    django.conf.urls.url(r'^coming-soon-campaign/$', django.views.generic.TemplateView.as_view(
        template_name='registration/coming_soon_campaign.html'), name='coming_soon_campaign'),
    django.conf.urls.url(r'^coming-soon-email/$', django.views.generic.TemplateView.as_view(
        template_name='registration/coming_soon_email.html'), name='coming_soon_email'),
    django.conf.urls.url(r'^reset-minor/$', views.ResetMinorCookieDocument.as_view(), name='reset_minor'),
    django.conf.urls.url(r'^terms-of-service/$', views.TermsOfServiceView.as_view(), name='terms_of_service'),
    django.conf.urls.url(r'^privacy-policy/$', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    django.conf.urls.url(r'^terms-of-service-by-state/$', views.TermsOfServiceByStateView.as_view(),
                         name='terms_of_service_by_state'),
    django.conf.urls.url(r'^register/(?P<step>.+)/$', views.RegistrationWizardView.as_view(
        url_name='register', done_step_name='complete'), name='register'),
    django.conf.urls.url(r'^revoke/$', views.RevokeView.as_view(), name='revoke'),
    django.conf.urls.url(r'^revoke-done/(?P<postal_code>[0-9]{5})/$', views.RevokeDoneView.as_view(), name='revoke_done'),
    django.conf.urls.url(r'^revoke-done/$', views.RevokeDoneView.as_view(), name='revoke_done'),
    django.conf.urls.url(r'^not-supported/$', views.UnsupportedStateView.as_view(), name='unsupported_state'),
    django.conf.urls.url(r'^redirect/$', views.StateRedirectView.as_view(), name='redirect_state'),
    django.conf.urls.url(r'^co-brand/$', views.CoBrandingView.as_view(), name='co_branding'),
    django.conf.urls.url(r'^co-brand-done/$', views.CoBrandingDoneView.as_view(), name='co_branding_done'),
)
