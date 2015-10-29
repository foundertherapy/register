from __future__ import unicode_literals

import django.contrib.admin

import models


@django.contrib.admin.register(models.WidgetSubmission)
class WidgetSubmissionAdmin(django.contrib.admin.ModelAdmin):
    search_fields = ('email', 'company_name', 'company_source',)
    list_display = ('email', 'company_name', 'company_source',)
    readonly_fields = ('company_source', 'created_on', 'updated_on',)
