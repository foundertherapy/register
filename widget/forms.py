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

from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger(__name__)
mark_safe_lazy = django.utils.functional.lazy(django.utils.safestring.mark_safe, django.utils.six.text_type)


def get_tos_label():
    return mark_safe_lazy(_('I agree to ORGANIZE&rsquo;s <a href="tos">Terms of Service</a>.'))


class WidgetCreateForm(django.forms.ModelForm):
    class Meta:
        model = models.WidgetSubmission
        fields = ['company_name', 'company_home_url', 'contact_name', 'contact_email', ]

    tos = django.forms.BooleanField(label=get_tos_label(), widget=django.forms.widgets.CheckboxInput(attrs={'required': 'required'}))

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
        raise django.forms.ValidationError(_('Enter a valid email.'))

    def clean_company_home_url(self):
        company_home_url = self.cleaned_data['company_home_url']
        validate_url = django.core.validators.URLValidator()
        try:
            validate_url(company_home_url)
        except django.core.exceptions.ValidationError:
            raise django.forms.ValidationError(_('Your company\'s URL format is not valid.'))

        return company_home_url
