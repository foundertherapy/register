from __future__ import unicode_literals

import django.conf
import django.conf.urls

import views

urlpatterns = django.conf.urls.patterns(
    '',
    django.conf.urls.url(r'^$', views.StateLookupView.as_view(), name='home'),
    django.conf.urls.url(
        r'^register/$', views.RegisterView.as_view(), name='register'),
    django.conf.urls.url(
        r'^register/complete/$',
        views.RegisterCompleteView.as_view(),
        name='register_complete'),
)
