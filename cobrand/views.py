from __future__ import unicode_literals

import logging
import urlparse
import cStringIO

import django.contrib.messages
import django.core.urlresolvers
import django.forms
import django.http
import django.shortcuts
import django.views.generic.edit
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from PIL import Image, ImageFile

import models
import forms
import emails


logger = logging.getLogger(__name__)


IMAGE_QUALITY = 75
THUMBNAIL_SIZE = (200, 100)


class CobrandCompanyCreateView(django.views.generic.edit.CreateView):
    template_name = 'cobrand/create.html'
    form_class = forms.CobrandCompanyCreateForm

    def post(self, request, *args, **kwargs):
        company_name = request.POST.get('company_name')
        if company_name:
            try:
                cobrand_company = models.CobrandCompany.objects.get(company_name=company_name)
                return django.shortcuts.redirect(cobrand_company.get_absolute_url())
            except models.CobrandCompany.DoesNotExist:
                pass
        return super(CobrandCompanyCreateView, self).post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CobrandCompanyCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Giving Tuesday Branded Registry'
        return context

    def get_success_url(self):
        return django.core.urlresolvers.reverse_lazy('cobrand_view', kwargs={'uuid': self.object.uuid, })

    def form_valid(self, form):
        response = super(CobrandCompanyCreateView, self).form_valid(form)
        company_logo = form.cleaned_data['company_logo']

        filename = '{}-original.png'.format(self.object.uuid)
        resized_filename = '{}.png'.format(self.object.uuid)

        # write the original
        default_storage.save('cobrand/{}'.format(filename), ContentFile(company_logo.read()))
        company_logo.seek(0)

        # resize the logo to create a thumbnail
        resized_company_logo = Image.open(ContentFile(company_logo.read()))
        resized_company_logo = resized_company_logo.convert(u'RGBA')
        resized_company_logo.thumbnail(THUMBNAIL_SIZE, Image.BICUBIC)
        io = cStringIO.StringIO()
        ImageFile.MAXBLOCK = max(resized_company_logo.size)**2
        resized_company_logo.save(io, format='PNG', quality=IMAGE_QUALITY, optimize=True, progressive=False)

        default_storage.save('cobrand/{}'.format(resized_filename), ContentFile(io.getvalue()))

        emails.send_admin_cobrand_register(cobrand_company=self.object)
        emails.send_cobrand_company_register_success(cobrand_company=self.object)

        return response


class CobrandCompanyDetailView(django.views.generic.DetailView):
    template_name = 'cobrand/detail.html'
    model = models.CobrandCompany
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_context_data(self, **kwargs):
        context = super(CobrandCompanyDetailView, self).get_context_data(**kwargs)
        context['title'] = 'Thanks for Signing Up for a Branded Registry Page!'

        parsed_url = urlparse.urlparse(self.request.build_absolute_uri())
        protocol = parsed_url.scheme
        domain = parsed_url.hostname
        port = parsed_url.port
        if port:
            host = ':'.join([domain, unicode(port)])
        else:
            host = domain
        context['company_redirect_url'] = '{}://{}{}'.format(protocol, host, self.object.get_redirect_url())

        return context


class CobrandRedirect(django.views.generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = kwargs['slug']
        try:
            cobrand_company = models.CobrandCompany.objects.get(slug=slug)
            return '/?cobrand_id={}'.format(cobrand_company.uuid)
        except models.CobrandCompany.DoesNotExist:
            return '/'
