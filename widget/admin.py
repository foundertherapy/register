from __future__ import unicode_literals

import django.contrib.admin
import django.contrib.sites.models

import models


@django.contrib.admin.register(models.WidgetSubmission)
class WidgetSubmissionAdmin(django.contrib.admin.ModelAdmin):
    list_display = ('company_name', 'company_home_url', 'created_on', 'updated_on', 'contact_email', 'contact_name', 'uuid', )
    search_fields = ('company_name', 'contact_email', 'contact_name', 'uuid', )
    ordering = ('-created_on', )
    fieldsets = (
        ('Status', {
            'fields': ('created_on', 'updated_on', 'uuid', ),
        }),
        ('Company Information', {
            'fields': ('company_name', 'company_home_url', 'contact_email', 'contact_name', ),
        }),
        ('Widget Information', {
            'fields': ('uuid', ),
        }),
    )
    readonly_fields = ('created_on', 'updated_on', 'uuid', )
