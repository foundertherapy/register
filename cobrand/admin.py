from __future__ import unicode_literals

import django.contrib.admin
import django.contrib.sites.models
from django.conf import settings

import models


@django.contrib.admin.register(models.CobrandCompany)
class CobrandCompanyAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('company_name', 'created_on', 'contact_email', 'contact_name', 'uuid', 'slug', )
    search_fields = ('company_name', 'contact_email', 'contact_name', 'uuid', )
    ordering = ('-created_on', )
    fieldsets = (
        ('Status', {
            'fields': ('created_on', 'updated_on', 'uuid', ),
        }),
        ('Company Information', {
            'fields': ('company_name', 'created_on', 'contact_email', 'contact_name', 'slug', ),
        }),
        ('Cobranding Information', {
            'fields': ('slug', 'cobrand_url', 'logo', ),
        }),
    )
    readonly_fields = ('created_on', 'updated_on', 'uuid', 'slug', 'cobrand_url', 'logo', )

    def cobrand_url(self, obj):
        return '<a href="{}">{}</a>'.format(obj.get_redirect_url(), obj.get_redirect_url())
    cobrand_url.short_description = 'Cobrand URL'
    cobrand_url.allow_tags = True
    cobrand_url.admin_order_field = 'slug'

    def logo(self, obj):
        return '<img src="{}cobrand/{}">'.format(settings.MEDIA_URL, obj.get_logo_filename())
    logo.short_description = 'Cobrand Logo'
    logo.allow_tags = True
    logo.admin_order_field = 'uuid'
