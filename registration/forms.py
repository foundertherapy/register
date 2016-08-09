from __future__ import unicode_literals

import logging
import re
import collections
import datetime

import django.forms
import django.forms.utils
import django.forms.widgets
import django.core.validators
import django.core.exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

import form_utils.forms
import requests
import dateutil.parser
import validate_email

from captcha import fields


logger = logging.getLogger(__name__)


REGISTRATION_CONFIGURATION_NAME = 'registration_configuration'

RE_NON_DECIMAL = re.compile(r'[^\d]+')
RE_NON_ALPHA = re.compile('[\W]+')
RE_POSTAL_CODE = re.compile(r'^[0-9]{5}$')
validate_postal_code = django.core.validators.RegexValidator(
    RE_POSTAL_CODE, _("Enter a valid postal code consisting 5 numbers."), 'invalid')


CHOICES_GENDER = (
    ('M', _('Male')),
    ('F', _('Female')),
)


class MultiEmailField(django.forms.CharField):
    message = _('Enter valid email addresses.')
    code = 'invalid'
    widget = django.forms.widgets.TextInput

    def to_python(self, value):
        "Normalize data to a list of strings."
        # Return None if no input was given.
        if not value:
            return []
        return [v.strip() for v in re.findall(validate_email.ADDR_SPEC, value)]

    def validate(self, value):
        "Check if value consists only of valid emails."

        # Use the parent's handling of required fields, etc.
        super(MultiEmailField, self).validate(value)
        try:
            for email in value:
                django.core.validators.validate_email(email)
        except django.core.exceptions.ValidationError:
            raise django.core.exceptions.ValidationError(self.message, code=self.code)


# This class was built to validate License ID format in server-side

# class CharRegexField(django.forms.CharField):
#     message = _('Please Enter a Valid License ID')
#     code = 'invalid'
#     widget = django.forms.widgets.TextInput
#     license_id_formats = None
#
#     def __init__(self, *args, **kwargs):
#         self.license_id_formats = kwargs['license_id_formats']
#         del kwargs['license_id_formats']
#         super(CharRegexField, self).__init__(*args, **kwargs)
#
#     def validate_license_id_formats(self, license_id):
#         valid_license_id = False
#         self.license_id_formats
#         regex_letter = '^[a-zA-Z]$'
#         regex_number = '^[0-9]$'
#         for license_id_format in self.license_id_formats:
#             if len(license_id_format) == len(license_id):
#                 alpha_numeric_match = True
#                 for index, alpha_num in enumerate(license_id_format):
#                     if (not((re.match(regex_letter, alpha_num) and re.match(
#                             regex_letter, license_id[index])) or(
#                                 re.match(regex_number, alpha_num) and
#                                 re.match(regex_number, license_id[index])))):
#                         alpha_numeric_match = False
#                         break
#                 if alpha_numeric_match:
#                     valid_license_id = True
#                     break
#             else:
#                 continue
#         return valid_license_id
#
#     def validate(self, value):
#         "Check if value match regular expression."
#         # Use the parent's handling of required fields, etc.
#         super(CharRegexField, self).validate(value)
#         if value:
#             if not self.validate_license_id_formats(value):
#                 raise django.core.exceptions.ValidationError(self.message, code=self.code)


class StateLookupForm(django.forms.Form):
    email = django.forms.EmailField(label=_('Email'), help_text=_('so we can send you confirmation of your registration'))
    postal_code = django.forms.CharField(
        label=_('Postal Code'),
        max_length=5, min_length=5, validators=[validate_postal_code],
        help_text=_('to determine which series of state-based questions we will ask next'))

    def clean_email(self):
        email = self.cleaned_data['email']
        if settings.DISABLE_EMAIL_VALIDATION:
            logger.warning('Email validation disabled: DISABLE_EMAIL_VALIDATION '
                           'is set')
            return email
        # use mailgun email address validator to check this email
        if not hasattr(settings, 'MAILGUN_PUBLIC_API_KEY'):
            logger.warning(
                'Cannot validate email: MAILGUN_PUBLIC_API_KEY not set')
            return email
        r = requests.get(
            'https://api.mailgun.net/v2/address/validate',
            data={'address': email, },
            auth=('api', settings.MAILGUN_PUBLIC_API_KEY))
        if r.status_code == 200:
            if r.json()['is_valid']:
                return email
        logger.warning('Cannot validate email: {}'.format(r.text))
        raise django.forms.ValidationError(_('Enter a valid email.'))


class UPENNStateLookupForm(StateLookupForm):
    error_css_class = 'invalid-data-error'
    email = django.forms.EmailField(label='')
    postal_code = django.forms.CharField(label='', max_length=5, min_length=5, validators=[validate_postal_code])

    email.widget.attrs['placeholder'] = 'EMAIL'
    email.widget.attrs['class'] = 'upenn-text-field'

    postal_code.widget.attrs['placeholder'] = 'POSTAL CODE'
    postal_code.widget.attrs['class'] = 'upenn-text-field'


def register_form_clean(self):
    cleaned_data = super(self.__class__, self).clean()

    if self.validate_organ_tissue_selection:
        organ_choices = [value for key, value in cleaned_data.items() if key.startswith('include')]
        if organ_choices:
            # For states like Arkansas, registrants will be asked to donate one organ/tissue only, without the ability to choose
            # the donation wishes for the other organs/tissues, deselecting that organ/tissue doesn't mean that they will not donate
            # any other parts.
            if not any(organ_choices):
                raise django.forms.ValidationError(_('At least one organ/tissue needs to be selected'))

    if self.api_errors and not self.skip_api_error_validation:
        # api_errors is a dict of field_name: [error text] that should be added
        # to each field if it is present
        for k, v in self.api_errors.items():
            if k in self.fields:
                self.add_error(k, v)

    return cleaned_data


def register_form_clean_license_id(self):
    license_id = self.cleaned_data['license_id']
    if self.fields['license_id'].required and is_license_id_not_applicable(license_id):
        raise django.forms.ValidationError(_('License ID is required.'))
    return license_id


def is_license_id_not_applicable(license_id):
    not_applicable_list = ['na', 'n/a', ]
    if license_id.lower() in not_applicable_list:
        return True
    return False


def register_form_clean_birthdate(self):
    date = self.cleaned_data['birthdate']
    if not date:
        return date
    if date >= datetime.date.today():
        raise django.forms.ValidationError(_('Enter an accurate birthdate.'))
    return date


def register_form_clean_phone_number(self):
    phone_number = self.cleaned_data['phone_number']
    if not phone_number:
        return phone_number
    phone_number = RE_NON_DECIMAL.sub('', phone_number)
    if phone_number.startswith('1'):
        phone_number = phone_number[1:]
    if len(phone_number) != 10:
        raise django.forms.ValidationError(
            _('Enter an accurate phone number including area code.'))
    return phone_number


def register_form_clean_ssn(self):
    ssn = self.cleaned_data['ssn']
    if not ssn:
        return ssn
    if len(ssn) != 4:
        raise django.forms.ValidationError(
            _('Enter the last 4 digits of your social security number.'))
    try:
        int(ssn)
    except ValueError:
        raise django.forms.ValidationError(_('Enter only digits.'))
    return ssn


def validate_date_generator(min_value):
    min_value = dateutil.parser.parse(min_value).date()

    def validate_date(date):
        if date < min_value:
            raise django.forms.ValidationError(
                _('Date must be later than %(date)s.') %
                {'date': min_value.strftime('%m/%d/%Y'), },
                code='minimum')

    return validate_date


def register_form_generator(conf):
    fieldsets = []
    fields = collections.OrderedDict()
    for index, fieldset_def in enumerate(conf['fieldsets']):
        fieldset_title = _(fieldset_def['title'])
        fieldset_fields = fieldset_def['fields']

        if not fieldset_fields:
            continue
        fieldset = (unicode(index), {'legend': fieldset_title, 'fields': []}, )

        has_booleans = False

        for field_def in fieldset_def['fields']:
            field_name = field_def['field_name']
            field_type = field_def.get('type')
            label = _(field_def['human_name']) or ''
            is_required = field_def.get('required', False)
            max_length = field_def.get('length')
            initial = field_def.get('default')
            if field_def.get('help_text'):
                help_text = _(field_def.get('help_text'))
            else:
                help_text = ''
            # process choices to add internationalization
            choices = field_def.get('choices')
            if choices:
                choices = [(a, _(b)) for a, b in choices]
            is_editable = field_def.get('editable', True)
            min_value = field_def.get('min_value')

            d = {
                'label': label,
            }

            if field_type == 'string':
                d['required'] = is_required
                d['initial'] = initial
                if choices and is_editable:
                    d['help_text'] = help_text
                    d['choices'] = choices
                    d['widget'] = django.forms.RadioSelect
                    field_class = django.forms.ChoiceField
                elif field_name == 'email':
                    d['max_length'] = max_length
                    d['help_text'] = help_text
                    field_class = django.forms.EmailField
                elif field_name == 'license_id' \
                        and 'license_id_formats' in conf:
                    d['max_length'] = max_length
                    license_id_formats = '{}{}{}'.format(
                            _('<p class=\'hint-license-id-format\'>Valid state License IDs should look like: '),
                            ', '.join(map(unicode, conf['license_id_formats'])), '</p>')
                    help_text = '{}{}{}'.format('<p> ', unicode(help_text), '</p>')
                    license_id_formats = '{}{}'.format(license_id_formats, help_text)
                    d['help_text'] = mark_safe(license_id_formats)
                    field_class = django.forms.CharField
                else:
                    d['max_length'] = max_length
                    d['help_text'] = help_text
                    field_class = django.forms.CharField
            elif field_type == 'date':
                d['required'] = is_required
                d['initial'] = initial
                d['help_text'] = help_text
                if min_value:
                    d['validators'] = [validate_date_generator(min_value), ]
                field_class = django.forms.DateField
            elif field_type == 'boolean':
                has_booleans = True
                d['initial'] = initial
                # this must be false otherwise checkbox must be checked
                if field_name == 'agree_to_tos':
                    d['help_text'] = mark_safe(help_text)
                    d['label'] = mark_safe(label)
                else:
                    d['required'] = False
                    d['help_text'] = help_text
                field_class = django.forms.BooleanField
            else:
                raise Exception('Unknown field type: {}'.format(field_type))

            fields[field_name] = field_class(**d)
            fieldset[1]['fields'].append(field_name)

            widget = fields[field_name].widget
            if not is_editable:
                if isinstance(widget, django.forms.Select):
                    widget.attrs['disabled'] = 'disabled'
                else:
                    widget.attrs['readonly'] = 'readonly'
            if field_type == 'date':
                widget.attrs['placeholder'] = '__/__/____'
                widget.attrs['class'] = 'date'
            if field_name == 'phone_number':
                widget.attrs['placeholder'] = '(___) ___-____'
                widget.attrs['class'] = 'phonenumber'
            if field_name == 'ssn':
                widget.attrs['placeholder'] = '____'
                widget.attrs['class'] = 'ssn'

        if has_booleans:
            fieldset[1]['classes'] = ['checkboxes', ]
        fieldsets.append(fieldset)

    cls_name = 'RegisterForm{}'.format(
        RE_NON_ALPHA.sub('', conf['title'].title())).encode(
        'ascii', errors='ignore')

    cls = type(
        cls_name,
        (form_utils.forms.BetterBaseForm, django.forms.BaseForm, ), {
            'base_fieldsets': fieldsets,
            'base_fields': fields,
            'base_row_attrs': {},
            'clean': register_form_clean,
            'clean_birthdate': register_form_clean_birthdate,
            'clean_phone_number': register_form_clean_phone_number,
            'clean_ssn': register_form_clean_ssn,
            'clean_license_id': register_form_clean_license_id,
            'api_errors': {},
            'skip_api_error_validation': False,
            'validate_organ_tissue_selection': conf.get('validate_organ_tissue_selection', None),
        })
    return cls


class RevokeForm(django.forms.Form):
    email = django.forms.EmailField(label=_('Email'))
    first_name = django.forms.CharField(
        label=_('First Name'), max_length=150, min_length=1)
    middle_name = django.forms.CharField(
        label=_('Middle Name'), max_length=150, min_length=0, required=False)
    last_name = django.forms.CharField(
        label=_('Last Name'), max_length=150, min_length=1)
    postal_code = django.forms.CharField(
        label=_('Postal Code'),
        max_length=5, min_length=5, validators=[validate_postal_code])
    gender = django.forms.ChoiceField(
        label=_('Gender'), choices=CHOICES_GENDER,
        widget=django.forms.RadioSelect)
    birthdate = django.forms.DateField(
        label=_('Birthdate'),
        widget=django.forms.DateInput(
            attrs={'placeholder': '__/__/____', 'class': 'date',}))
    # agree_to_tos = django.forms.BooleanField(
    #     label=mark_safe(_('In order to revoke my organ and tissue donation status through Organize, I agree to ORGANIZE\'s '
    #                       '<a href="#" onClick="window.open(\'/terms-of-service/\', \'_blank\', \'width=900,height=900\')'
    #                       '">Terms of Service</a> and <a href="#" onClick="window.open(\'/privacy-policy/\', \'_blank\', '
    #                       '\'width=900,height=900\')">Privacy Policy</a>.')),
    #     widget=django.forms.widgets.CheckboxInput(
    #         attrs={'required': 'required', }))
    agree_to_tos = django.forms.BooleanField(label='', widget=django.forms.widgets.CheckboxInput(attrs={'required': 'required', }))

    def clean_email(self):
        email = self.cleaned_data['email']
        if settings.DISABLE_EMAIL_VALIDATION:
            logger.warning(
                'Email validation disabled: DISABLE_EMAIL_VALIDATION is set')
            return email
        # use mailgun email address validator to check this email
        if not hasattr(settings, 'MAILGUN_PUBLIC_API_KEY'):
            logger.warning(
                'Cannot validate email: MAILGUN_PUBLIC_API_KEY not set')
            return email
        r = requests.get(
            'https://api.mailgun.net/v2/address/validate',
            data={'address': email, },
            auth=('api', settings.MAILGUN_PUBLIC_API_KEY))
        if r.status_code == 200:
            if r.json()['is_valid']:
                return email
        logger.warning('Cannot validate email: {}'.format(r.text))
        raise django.forms.ValidationError(_('Enter a valid email.'))


class EmailNextOfKinForm(django.forms.Form):
    to = MultiEmailField(label=_('To'), max_length=300, help_text=_('Enter one or more emails separated by commas.'))
    subject = django.forms.CharField(label=_('Subject'), max_length=250)
    body = django.forms.CharField(label=_('Body'), widget=django.forms.widgets.Textarea())

    def clean_to(self):
        emails = self.cleaned_data['to']
        if settings.DISABLE_EMAIL_VALIDATION:
            logger.warning('Email validation disabled: DISABLE_EMAIL_VALIDATION is set')
            return emails
        # use mailgun email address validator to check this email
        if not hasattr(settings, 'MAILGUN_PUBLIC_API_KEY'):
            logger.warning('Cannot validate email: MAILGUN_PUBLIC_API_KEY not set')
            return emails
        valid_emails = []
        invalid_emails = []
        for email in emails:
            r = requests.get('https://api.mailgun.net/v2/address/validate',
                             data={'address': email, },
                             auth=('api', settings.MAILGUN_PUBLIC_API_KEY))
            if r.status_code == 200 and r.json()['is_valid']:
                valid_emails.append(email)
            else:
                logger.warning('Cannot validate email: {}'.format(r.text))
                invalid_emails.append(email)
        if invalid_emails:
            raise django.forms.ValidationError(_('Enter valid email addresses.'))
        else:
            return valid_emails


class CaptchaForm(django.forms.Form):
    captcha = fields.CaptchaField()
