from __future__ import unicode_literals

import logging

import django.forms
import django.forms.utils
import django.forms.widgets
import django.conf
import django.core.validators
import django.core.exceptions
import django.utils.functional
import django.utils.safestring
import django.utils.six

import requests

import models


logger = logging.getLogger(__name__)


class WidgetCreateForm(django.forms.ModelForm):
    tos = django.forms.BooleanField(
        label=django.utils.safestring.mark_safe(
            'I agree to ORGANIZE&rsquo;s <a href="tos">Terms of Service</a>.'
        ),
        widget=django.forms.widgets.CheckboxInput(attrs={'required': 'required'}))

    class Meta:
        model = models.WidgetHost
        fields = ['contact_name', 'contact_email', 'host_url', ]

    def clean_email(self):
        contact_email = self.cleaned_data['contact_email']
        if django.conf.settings.DISABLE_EMAIL_VALIDATION:
            logger.warning('Email validation disabled: DISABLE_EMAIL_VALIDATION is set')
            return contact_email
        # use mailgun email address validator to check this email
        if not hasattr(django.conf.settings, 'MAILGUN_PUBLIC_API_KEY'):
            logger.warning('Cannot validate email: MAILGUN_PUBLIC_API_KEY not set')
            return contact_email
        r = requests.get('https://api.mailgun.net/v2/address/validate', data={'address': contact_email, },
                         auth=('api', django.conf.settings.MAILGUN_PUBLIC_API_KEY))
        if r.status_code == 200:
            if r.json()['is_valid']:
                return contact_email
        logger.warning('Cannot validate email: {}'.format(r.text))
        raise django.forms.ValidationError('Enter a valid email.')
