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
import emails


logger = logging.getLogger(__name__)


class WidgetCreateView(django.views.generic.edit.CreateView):
    template_name = 'widget/create.html'
    form_class = forms.WidgetCreateForm

    def get_context_data(self, **kwargs):
        context = super(WidgetCreateView, self).get_context_data(**kwargs)
        context['title'] = _('Giving Tuesday Embedded Registration')
        return context

    def form_valid(self, form):
        response = super(WidgetCreateView, self).form_valid(form)

        emails.send_admin_widget_register(widget_host=self.object)
        emails.send_widget_register_success(widget_host=self.object)

        return response

    def get_success_url(self):
        return django.core.urlresolvers.reverse_lazy('widget_view', kwargs={'uuid': self.object.uuid, })


class WidgetDetailView(django.views.generic.TemplateView):
    template_name = 'widget/detail.html'

    def get_context_data(self, **kwargs):
        context = super(WidgetDetailView, self).get_context_data(**kwargs)
        context['title'] = _('Thanks for Signing Up for an Embedded Registration Button!')
        return context
