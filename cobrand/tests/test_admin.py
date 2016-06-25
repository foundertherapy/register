from __future__ import unicode_literals

import os

import django.test
import django.test.client
import django.test.utils
import django.conf
import django.contrib.admin.sites

from .. import models
from .. import admin
import accounts.models


class CobrandCompanyAdminTestCase(django.test.TestCase):
    fixtures = ('test_users.json', 'test_companies.json', 'test_cobrand_companies.json', )

    def setUp(self):
        self.superuser = accounts.models.User.objects.get(pk=1)
        self.cobrand_companies = list(models.CobrandCompany.objects.order_by('pk'))
        self.cobrand_company_admin = admin.CobrandCompanyAdmin(models.CobrandCompany, django.contrib.admin.sites.AdminSite())

    def test_change_view(self):
        c = django.test.Client()
        c.force_login(self.superuser)
        response = c.get('/admin/cobrand/cobrandcompany/1/change/')
        self.assertEqual(response.status_code, 200)
        # test for the fields that are shown
        self.assertSetEqual(set(response.context['adminform'].readonly_fields),
                            {'created_on', 'updated_on', 'uuid', 'slug', 'cobrand_url', 'logo', })
        # Test that the fields company name, contact email, and contact name are editable
        self.assertListEqual(response.context['adminform'].form.fields.keys(),
                             ['company_name', 'contact_email', 'contact_name', ])

    def test_change_view_save(self):
        c = django.test.Client()
        c.force_login(self.superuser)
        data = {'company_name': 'foo', 'contact_email': 'b@b.com', 'contact_name': 'another name', }
        response = c.post('/admin/cobrand/cobrandcompany/1/change/', data=data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/cobrand/cobrandcompany/', )
