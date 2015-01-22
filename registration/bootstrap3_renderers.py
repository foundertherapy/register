import bootstrap3.renderers

from django.template.loader import get_template
from django.template import Context
from bootstrap3.forms import render_tag


class FiftyThreeFieldRenderer(bootstrap3.renderers.FieldRenderer):
    def append_to_field(self, html):
        if self.field_errors:
            help_html = get_template(
                'bootstrap3/field_help_text_and_errors.html'
            ).render(Context({
                'field': self.field,
                'help_text_and_errors': self.field_errors,
                'layout': self.layout,
            }))
            html += '<span class="help-block">{help}</span>'.format(
                help=help_html)

        if self.field_help:
            attrs = {
                'class': 'fa fa-question field-help',
                'data-toggle': "popover",
                'data-content': self.field_help,
                'data-trigger': 'hover',
                'data-placement': 'auto',
                'data-title': 'Help for {}'.format(self.field.label), }
            html = render_tag('i', attrs=attrs) + html
        return html


