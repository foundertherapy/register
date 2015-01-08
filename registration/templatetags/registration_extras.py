from django import template

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
