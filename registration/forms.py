from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django.forms.utils import ErrorList
import django.forms


class StateLookupForm(django.forms.Form):
    email = django.forms.EmailField()
    postal_code = django.forms.CharField(max_length=5, min_length=5)


class RegisterForm(django.forms.Form):
    # first_name = django.forms.CharField(max_length=50)
    # middle_name = django.forms.CharField(max_length=50, required=False)
    # last_name = django.forms.CharField(max_length=50)
    # email = django.forms.EmailField()
    # birthdate = django.forms.DateField()
    # street_address = django.forms.CharField(max_length=100, required=False)
    # city = django.forms.CharField(max_length=100)
    # state = django.forms.CharField(max_length=2)
    # postal_code = django.forms.CharField(max_length=5, min_length=5)
    # license_id = django.forms.CharField(max_length=15)
    def __init__(self, fields=None, data=None, files=None, auto_id='id_%s',
                 prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, ):
        super(RegisterForm, self).__init__(
            data=data, files=files, auto_id=auto_id, prefix=prefix,
            initial=initial, error_class=error_class, label_suffix=label_suffix,
            empty_permitted=empty_permitted)

        if fields:
            print fields
            for field_name, field_def in fields.items():
                d = {
                    'label': field_def.get('name', ''),
                    'required': field_def.get('required', False)
                }
                if 'choices' in field_def:
                    choices = field_def.get('choices')
                    if choices:
                        choices = zip(choices, choices)
                        d['choices'] = choices
                elif 'max_length' in field_def:
                    d['max_length'] = field_def.get('max_length')

                field_class = self.get_field_class(field_def)
                self.fields[field_name] = field_class(**d)

    def get_field_class(self, field_def):
        field_type = field_def.get('type', 'string')
        has_choices = field_def.get('choices')

        if field_type == 'string' and not has_choices:
            return django.forms.CharField
        elif field_type == 'string' and has_choices:
            return django.forms.ChoiceField
        else:
            return django.forms.Field
