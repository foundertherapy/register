from __future__ import unicode_literals

import logging
import django.db.models
import django.core.cache


logger = logging.getLogger(__name__)


class CoBrandingRegistration(django.db.models.Model):
    email = django.db.models.EmailField()
    company_name = django.db.models.CharField(max_length=30)
    company_logo = django.db.models.CharField(max_length=255, blank=True, null=True)
    company_home_url = django.db.models.CharField(max_length=255, blank=True, null=True)
    co_branding_id = django.db.models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.company_name)
