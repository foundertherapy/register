from django import template

import phonenumbers
import phonenumbers.phonenumberutil

register = template.Library()


@register.filter
def tabindex(value, index):
    """
    Add a tabindex attribute to the widget for a bound field.
    """
    value.field.widget.attrs['tabindex'] = index
    return value


@register.filter
def key(d, k):
    return d.get(k)


@register.filter
def phonenumber(p):
    try:
        phone_number = phonenumbers.parse(p, 'US')
        return phonenumbers.format_number(
            phone_number, phonenumbers.PhoneNumberFormat.NATIONAL)
    except phonenumbers.phonenumberutil.NumberParseException:
        return p
