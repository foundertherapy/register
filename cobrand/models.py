from __future__ import unicode_literals

import logging

import django.db.models
import django.core.cache
from django.template.defaultfilters import slugify
import django.core.urlresolvers

import shortuuidfield


logger = logging.getLogger(__name__)


class CobrandCompany(django.db.models.Model):
    created_on = django.db.models.DateTimeField(auto_now_add=True)
    updated_on = django.db.models.DateTimeField(auto_now=True)

    company_name = django.db.models.CharField(max_length=100, unique=True, db_index=True)
    contact_email = django.db.models.EmailField()
    contact_name = django.db.models.CharField(max_length=200)
    uuid = shortuuidfield.ShortUUIDField(auto=True, unique=True, db_index=True)
    slug = django.db.models.SlugField(unique=True, db_index=True, editable=False)

    class Meta:
        verbose_name_plural = 'Cobrand Companies'
        verbose_name = 'Cobrand Company'

    def __unicode__(self):
        return unicode(self.company_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.company_name)
        super(CobrandCompany, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return django.core.urlresolvers.reverse('cobrand_view', args=[self.uuid, ])

    def get_redirect_url(self):
        return django.core.urlresolvers.reverse('cobrand_redirect', kwargs={'slug': self.slug, })

    def get_logo_filename(self):
        return '{}.png'.format(self.uuid)

