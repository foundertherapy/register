from __future__ import unicode_literals

import logging

import django.contrib.messages
import django.core.urlresolvers
import django.forms
import django.http
import django.shortcuts
import django.views.generic.edit
from django.utils.translation import ugettext_lazy as _

import forms


logger = logging.getLogger(__name__)


class WidgetCreateView(django.views.generic.edit.CreateView):
    template_name = 'widget/create.html'
    form_class = forms.WidgetCreateForm

    def get_success_url(self):
        return django.core.urlresolvers.reverse_lazy('widget_view', kwargs={'uuid': self.object.uuid, })


class WidgetSelectView(django.views.generic.TemplateView):
    template_name = 'widget/select.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetSelectView, self).get_context_data()
        context['page_title'] = _('Configure your Widget')
        context['widget_id'] = self.kwargs['uuid']

        return context