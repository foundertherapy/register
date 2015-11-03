from __future__ import unicode_literals

import django.db.models
import django.core.cache
import shortuuidfield
import shortuuid

from django.utils.translation import ugettext_lazy as _


class WidgetSubmission(django.db.models.Model):
    email = django.db.models.EmailField(blank=False, null=False)
    company_name = django.db.models.CharField(max_length=30, blank=False, null=False)
    company_source = shortuuidfield.ShortUUIDField(_('Company Source'), db_index=True, blank=False, null=False)
    home_page_url = django.db.models.CharField(max_length=255, blank=True, null=True)
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.company_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.company_source = shortuuid.uuid()
        super(WidgetSubmission, self).save(force_insert, force_update, using, update_fields)