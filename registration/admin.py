from __future__ import unicode_literals

import django.contrib.admin

import models


@django.contrib.admin.register(models.WidgetSubmission)
class WidgetSubmissionAdmin(django.contrib.admin.ModelAdmin):
    search_fields = ('email', 'company_name', 'widget_id',)
    list_display = ('email', 'company_name', 'widget_id',)
    readonly_fields = ('widget_id', 'created_on', 'updated_on',)
