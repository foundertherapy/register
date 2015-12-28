import re

from django.forms import (
    CheckboxInput, ClearableFileInput, RadioSelect, CheckboxSelectMultiple
)
from django.forms.widgets import SelectDateWidget
from django.utils.html import strip_tags

import bootstrap3.renderers
from bootstrap3.forms import render_label


RE_INPUT_TAG = re.compile(r'(<label.*>)(<input.*/>)')


class FiftyThreeFieldRenderer(bootstrap3.renderers.FieldRenderer):
    def post_widget_render(self, html):
        if isinstance(self.widget, RadioSelect):
            html = self.list_to_class(html, 'radio')
            html = self.invert_radio_input(html)
        elif isinstance(self.widget, CheckboxSelectMultiple):
            html = self.list_to_class(html, 'checkbox')
        elif isinstance(self.widget, SelectDateWidget):
            html = self.fix_date_select_input(html)
        elif isinstance(self.widget, ClearableFileInput):
            html = self.fix_clearable_file_input(html)
        elif isinstance(self.widget, CheckboxInput):
            html = self.put_inside_label(html)
        return html

    def put_inside_label(self, html):
        return html + render_label(
            content=self.field.label, label_for=self.field.id_for_label,
            label_title=strip_tags(self.field_help))

    def invert_radio_input(self, html):
        # NOTE: THIS IS A KLUDGE!
        # find the input tag
        return re.sub(RE_INPUT_TAG, r'\2\1', html)
