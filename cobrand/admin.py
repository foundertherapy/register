from __future__ import unicode_literals

import django.contrib.admin
import django.contrib.sites.models
import django.utils.safestring
from django.conf import settings

import models
import emails


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
            'fields': ('company_name', 'contact_email', 'contact_name', ),
        }),
        ('Cobranding Information', {
            'fields': ('slug', 'cobrand_url', 'logo', ),
        }),
    )
    readonly_fields = ('created_on', 'updated_on', 'uuid', 'slug', 'cobrand_url', 'logo', )
    actions = ['send_cobrand_register_success_email', ]

    def cobrand_url(self, obj):
        return django.utils.safestring.mark_safe('<a href="{}">{}</a>'.format(obj.get_redirect_url(), obj.get_redirect_url()))
    cobrand_url.short_description = 'Cobrand URL'
    cobrand_url.admin_order_field = 'slug'

    def logo(self, obj):
        return django.utils.safestring.mark_safe('<img src="{}cobrand/{}">'.format(settings.MEDIA_URL, obj.get_logo_filename()))
    logo.short_description = 'Cobrand Logo'

    logo.admin_order_field = 'uuid'

    def send_cobrand_register_success_email(self, request, queryset):
        count = 0

        for cobrand_company in queryset.all():
            emails.send_cobrand_company_register_success(cobrand_company=cobrand_company)
            count += 1
        if count == 1:
            bit = '1 cobrand register success email'
        else:
            bit = '{} cobrand register successs'.format(count)
        self.message_user(request, '{} sent'.format(bit))
    send_cobrand_register_success_email.short_description = \
        'Send cobrand register success email'
