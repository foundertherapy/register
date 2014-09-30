from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
import django.forms


class StateLookupForm(django.forms.Form):
    email = django.forms.EmailField()
    postal_code = django.forms.CharField(max_length=5, min_length=5)


class RegisterForm(django.forms.Form):
    first_name = django.forms.CharField(max_length=50)
    middle_name = django.forms.CharField(max_length=50, required=False)
    last_name = django.forms.CharField(max_length=50)
    email = django.forms.EmailField()
    birthdate = django.forms.DateField()
    street_address = django.forms.CharField(max_length=100, required=False)
    city = django.forms.CharField(max_length=100)
    state = django.forms.CharField(max_length=2)
    postal_code = django.forms.CharField(max_length=5, min_length=5)
    license_id = django.forms.CharField(max_length=15)
