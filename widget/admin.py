from __future__ import unicode_literals

import django.contrib.admin
import django.contrib.sites.models

import models


@django.contrib.admin.register(models.WidgetHost)
class WidgetHostAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('uuid', 'host_url', 'created_on', 'contact_email', 'contact_name', )
    search_fields = ('host_url', 'contact_email', 'contact_name', 'uuid', )
    ordering = ('-created_on', )
    fieldsets = (
        ('Status', {
            'fields': ('created_on', 'updated_on', 'uuid', ),
        }),
        ('Company Information', {
            'fields': ('contact_email', 'contact_name', 'host_url', ),
        }),
    )
    readonly_fields = ('created_on', 'updated_on', 'uuid', )
