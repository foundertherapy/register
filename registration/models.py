from __future__ import unicode_literals

import logging
import django.db.models
import django.core.cache
import shortuuidfield
import shortuuid


logger = logging.getLogger(__name__)


class CoBrandingRegistration(django.db.models.Model):
    email = django.db.models.EmailField()
    company_name = django.db.models.CharField(max_length=30)
    company_home_url = django.db.models.CharField(max_length=255, blank=True, null=True)
    cobrand_id = shortuuidfield.ShortUUIDField(db_index=True, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.company_name)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.cobrand_id = shortuuid.uuid()
        super(CoBrandingRegistration, self).save(force_insert, force_update, using, update_fields)
