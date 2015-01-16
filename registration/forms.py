from __future__ import unicode_literals

import logging
import re
import collections

from django.utils.translation import ugettext_lazy as _
import django.forms
import django.core.validators

import form_utils.forms

logger = logging.getLogger(__name__)

REGISTRATION_CONFIGURATION_NAME = 'registration_configuration'

RE_NON_ALPHA = re.compile('[\W]+')
RE_POSTAL_CODE = re.compile(r'^[0-9]{5}$')
validate_postal_code = django.core.validators.RegexValidator(
    RE_POSTAL_CODE, _("Enter a valid postal code consisting 5 numbers."),
    'invalid')


class StateLookupForm(django.forms.Form):
    email = django.forms.EmailField()
    postal_code = django.forms.CharField(
        max_length=5, min_length=5, validators=[validate_postal_code])


def register_form_clean(self):
    cleaned_data = super(self.__class__, self).clean()
    if self.api_errors and not self.skip_api_error_validation:
        # api_errors is a dict of field_name: [error text] that should be added
        # to each field if it is present
        for k, v in self.api_errors.items():
            if k in self.fields:
                self.add_error(k, v)
    return cleaned_data


def register_form_generator(conf):
    fieldsets = []
    fields = collections.OrderedDict()
    for index, fieldset_def in enumerate(conf['fieldsets']):
        fieldset_title = fieldset_def['title']
        fieldset_fields = fieldset_def['fields']
        if not fieldset_fields:
            continue
        fieldset = (unicode(index), {
            'legend': fieldset_title,
            'fields': []}, )

        for field_def in fieldset_def['fields']:
            field_name = field_def['field_name']
            field_type = field_def.get('type')
            label = field_def['human_name']
            is_required = field_def.get('required', False)
            max_length = field_def.get('length')
            initial = field_def.get('default')
            help_text = field_def.get('help_text')
            choices = field_def.get('choices')
            is_editable = field_def.get('editable', True)

            d = {
                'label': label,
            }

            if field_type == 'string' and choices and is_editable:
                d['required'] = is_required
                d['initial'] = initial
                d['help_text'] = help_text
                d['choices'] = choices
                d['widget'] = django.forms.RadioSelect
                field_class = django.forms.ChoiceField
            elif field_type == 'string' and field_name == 'email':
                d['required'] = is_required
                d['max_length'] = max_length
                d['initial'] = initial
                d['help_text'] = help_text
                field_class = django.forms.EmailField
            elif field_type == 'string':
                d['required'] = is_required
                d['max_length'] = max_length
                d['initial'] = initial
                d['help_text'] = help_text
                field_class = django.forms.CharField
            elif field_type == 'date':
                d['required'] = is_required
                d['initial'] = initial
                d['help_text'] = help_text
                field_class = django.forms.DateField
            elif field_type == 'boolean':
                d['initial'] = initial
                # this must be false otherwise checkbox must be checked
                if field_name != 'agree_to_tos':
                    d['required'] = False
                    d['help_text'] = help_text
                field_class = django.forms.BooleanField
            else:
                raise Exception('Unknown field type: {}'.format(field_type))

            fields[field_name] = field_class(**d)
            fieldset[1]['fields'].append(field_name)

            if not is_editable:
                widget = fields[field_name].widget
                if isinstance(widget, django.forms.Select):
                    widget.attrs['disabled'] = 'disabled'
                else:
                    widget.attrs['readonly'] = 'readonly'
        fieldsets.append(fieldset)

    cls_name = 'RegisterForm{}'.format(
        RE_NON_ALPHA.sub('', conf['title'].title())).encode(
        'ascii', errors='ignore')
    cls = type(
        cls_name,
        (form_utils.forms.BetterBaseForm, django.forms.BaseForm, ),
        {'base_fieldsets': fieldsets, 'base_fields': fields,
         'base_row_attrs': {}, 'clean': register_form_clean,
         'api_errors': {}, 'skip_api_error_validation': False, })
    return cls
