from __future__ import unicode_literals

import os

import django.test
import django.test.utils
import django.core.mail
import django.conf

from .. import models
from .. import forms


TEST_FILENAME = os.path.join(os.path.dirname(__file__), 'test.jpeg')


class CobrandCompanyCreateViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_get(self):
        r = self.client.get('/brand/', follow=False)
        self.assertEqual(r.status_code, 200)
        # make sure there's a form on this page with the right fields
        self.assertTemplateUsed(r, 'cobrand/create.html')
        self.assertIsInstance(r.context['form'], forms.CobrandCompanyCreateForm)

    def test_post_no_data(self):
        data = {}
        r = self.client.post('/brand/', data=data)
        self.assertEqual(r.status_code, 200)
        # make sure there's a form on this page with the right fields
        self.assertTemplateUsed(r, 'cobrand/create.html')
        self.assertIsInstance(r.context['form'], forms.CobrandCompanyCreateForm)
        self.assertFormError(r, 'form', 'company_name', 'This field is required.')
        self.assertFormError(r, 'form', 'contact_name', 'This field is required.')
        self.assertFormError(r, 'form', 'contact_email', 'This field is required.')
        self.assertFormError(r, 'form', 'company_logo', 'This field is required.')
        self.assertFormError(r, 'form', 'tos', 'This field is required.')

    def test_post_full_data(self):
        with open(TEST_FILENAME) as test_file:
            data = {
                'company_name': 'Test Company',
                'contact_name': 'Test Contact',
                'contact_email': 'test@example.com',
                'company_logo': test_file,
                'tos': True,
            }
            r = self.client.post('/brand/', data=data)
        cobrand_company_uuid = r.url.split('/')[-2]
        self.assertRedirects(r, '/brand/{}/'.format(cobrand_company_uuid))
        # make sure the object was properly saved
        cobrand_company = models.CobrandCompany.objects.get(uuid=cobrand_company_uuid)
        # make sure an email was sent for admin and for user notification
        self.assertEqual(len(django.core.mail.outbox), 2)
        self.assertEqual(django.core.mail.outbox[0].to, map(lambda x: x[1], django.conf.settings.ADMINS))
        self.assertEqual(django.core.mail.outbox[1].to, ['test@example.com', ])

    def test_post_duplicate_data(self):
        with open(TEST_FILENAME) as test_file:
            data = {
                'company_name': 'Test Company',
                'contact_name': 'Test Contact',
                'contact_email': 'test@example.com',
                'company_logo': test_file,
                'tos': True,
            }
            r = self.client.post('/brand/', data=data)
            r = self.client.post('/brand/', data=data)
        self.assertEqual(r.status_code, 302)

        cobrand_company_uuid = r.url.split('/')[-2]
        # make sure the object was properly redirected
        cobrand_company = models.CobrandCompany.objects.get(uuid=cobrand_company_uuid)
        self.assertEquals(cobrand_company.company_name, 'Test Company')
