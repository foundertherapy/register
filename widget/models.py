from __future__ import unicode_literals

import logging

import django.db.models
import django.core.cache
import django.core.urlresolvers

import shortuuidfield


logger = logging.getLogger(__name__)


class WidgetSubmission(django.db.models.Model):
    contact_email = django.db.models.EmailField()
    contact_name = django.db.models.CharField(max_length=200)
    company_name = django.db.models.CharField(max_length=100, unique=True, db_index=True)
    company_home_url = django.db.models.CharField(max_length=255)
    uuid = shortuuidfield.ShortUUIDField(auto=True, unique=True, db_index=True)

    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Widget Companies'
        verbose_name = 'Widget Company'

    def __unicode__(self):
        return unicode(self.company_name)

    def get_absolute_url(self):
        return django.core.urlresolvers.reverse_lazy('widget_view', kwargs={'uuid': self.uuid, })
