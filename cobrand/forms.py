from __future__ import unicode_literals

import logging

import django.forms
import django.forms.utils
import django.forms.widgets
import django.template.defaultfilters
import django.conf
import django.utils.six  # Python 3 compatibility
import django.utils.safestring
import django.utils.functional
import django.core.urlresolvers


import requests

import models


logger = logging.getLogger(__name__)


class CobrandCompanyCreateForm(django.forms.ModelForm):
    company_logo = django.forms.ImageField(
        label='Company Logo',
        help_text='Upload a logo for your company in either JPEG or PNG format.')
    tos = django.forms.BooleanField(
        label=django.utils.safestring.mark_safe('I agree to ORGANIZE&rsquo;s <a href="tos">Terms of Service</a>.'),
        widget=django.forms.widgets.CheckboxInput(attrs={'required': 'required'}))
    invalid_company_name = 'This Company Name is Already Exists'

    class Meta:
        model = models.CobrandCompany
        fields = ['company_name', 'contact_name', 'contact_email', ]

    def clean_email(self):
        email = self.cleaned_data['email']
        if django.conf.settings.DISABLE_EMAIL_VALIDATION:
            logger.warning('Email validation disabled: DISABLE_EMAIL_VALIDATION is set')
            return email
        # use mailgun email address validator to check this email
        if not hasattr(django.conf.settings, 'MAILGUN_PUBLIC_API_KEY'):
            logger.warning('Cannot validate email: MAILGUN_PUBLIC_API_KEY not set')
            return email
        r = requests.get(
            'https://api.mailgun.net/v2/address/validate',
            data={'address': email, },
            auth=('api', django.conf.settings.MAILGUN_PUBLIC_API_KEY))
        if r.status_code == 200:
            if r.json()['is_valid']:
                return email
        logger.warning('Cannot validate email: {}'.format(r.text))
        raise django.forms.ValidationError('Enter a valid email.')

    def clean_company_name(self):
        company_name = self.cleaned_data['company_name']
        company_name_slug = django.template.defaultfilters.slugify(company_name)

        if models.CobrandCompany.objects.filter(slug__iexact=company_name_slug).exists():
            raise django.forms.ValidationError(self.invalid_company_name)

        return company_name
