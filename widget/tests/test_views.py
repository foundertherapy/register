from __future__ import unicode_literals


import django.test
import django.test.utils
import django.core.mail
import django.conf

from .. import models
from .. import forms


class WidgetHostCreateViewTestCase(django.test.TestCase):
    def setUp(self):
        self.client = django.test.Client()

    def test_get(self):
        r = self.client.get('/widget/', follow=False)
        self.assertEqual(r.status_code, 200)
        # make sure there's a form on this page with the right fields
        self.assertTemplateUsed(r, 'widget/create.html')
        self.assertIsInstance(r.context['form'], forms.WidgetCreateForm)

    def test_post_no_data(self):
        data = {}
        r = self.client.post('/widget/', data=data)
        self.assertEqual(r.status_code, 200)
        # make sure there's a form on this page with the right fields
        self.assertTemplateUsed(r, 'widget/create.html')
        self.assertIsInstance(r.context['form'], forms.WidgetCreateForm)
        self.assertFormError(r, 'form', 'contact_name', 'This field is required.')
        self.assertFormError(r, 'form', 'contact_email', 'This field is required.')
        self.assertFormError(r, 'form', 'host_url', 'This field is required.')
        self.assertFormError(r, 'form', 'tos', 'This field is required.')

    def test_post_full_data(self):

        data = {
            'contact_name': 'Test Contact',
            'contact_email': 'test@example.com',
            'host_url': 'http://www.organize.org',
            'tos': True,
        }
        r = self.client.post('/widget/', data=data)

        widget_host_uuid = r.url.split('/')[-2]
        self.assertRedirects(r, '/widget/{}/'.format(widget_host_uuid))
        # make sure the object was properly saved
        models.WidgetHost.objects.get(uuid=widget_host_uuid)
        # make sure an email was sent for admin and for user notification
        self.assertEqual(len(django.core.mail.outbox), 2)
        self.assertEqual(django.core.mail.outbox[0].to, map(lambda x: x[1], django.conf.settings.ADMINS))
        self.assertEqual(django.core.mail.outbox[1].to, ['test@example.com', ])

    def test_post_duplicate_data(self):
        data = {
            'contact_name': 'Test Contact',
            'contact_email': 'test@example.com',
            'host_url': 'http://www.organize.org',
            'tos': True,
        }
        r = self.client.post('/widget/', data=data)
        r = self.client.post('/widget/', data=data)
        self.assertEqual(r.status_code, 302)

        widget_host_uuid = r.url.split('/')[-2]
        # make sure the object was properly redirected
        widget_host = models.WidgetHost.objects.get(uuid=widget_host_uuid)
        self.assertEquals(widget_host.host_url, 'http://www.organize.org')
