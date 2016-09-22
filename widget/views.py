from __future__ import unicode_literals

import logging

import django.contrib.messages
import django.urls
import django.forms
import django.http
import django.shortcuts
import django.views.generic.edit

import forms
import emails
import models


logger = logging.getLogger(__name__)


class WidgetCreateView(django.views.generic.edit.CreateView):
    template_name = 'widget/create.html'
    form_class = forms.WidgetCreateForm

    def post(self, request, *args, **kwargs):
        host_url = request.POST.get('host_url')
        if host_url:
            if models.WidgetHost.objects.filter(host_url=host_url).exists():
                widget_host = models.WidgetHost.objects.get(host_url=host_url)
                return django.shortcuts.redirect(widget_host.get_absolute_url())

        return super(WidgetCreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        response = super(WidgetCreateView, self).form_valid(form)

        emails.send_admin_widget_register(widget_host=self.object)
        emails.send_widget_register_success(widget_host=self.object)

        return response

    def get_success_url(self):
        return django.urls.reverse_lazy('widget_view', kwargs={'uuid': self.object.uuid, })


class WidgetDetailView(django.views.generic.TemplateView):
    template_name = 'widget/detail.html'
