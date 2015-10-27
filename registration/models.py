from __future__ import unicode_literals

import logging
import django.db.models
import django.core.cache
import shortuuidfield
import shortuuid

from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)


class WidgetSubmission(django.db.models.Model):
    email = django.db.models.EmailField()
    company_name = django.db.models.CharField(max_length=30)
    company_source = shortuuidfield.ShortUUIDField(_('Company Source'), db_index=True)

    def __unicode__(self):
        return unicode(self.company_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.company_source = shortuuid.uuid()
        super(WidgetSubmission, self).save(force_insert, force_update, using, update_fields)