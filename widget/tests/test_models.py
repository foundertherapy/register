from __future__ import unicode_literals

import django.db

from django.test import TestCase

from widget import models


class WidgetHostTestCase(TestCase):
    def test_unique(self):
        # ensure company_name is unique
        models.WidgetHost.objects.create(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        self.assertRaises(
            django.db.IntegrityError,
            lambda: models.WidgetHost.objects.create(contact_email='a@a.com', contact_name='test user', host_url='http://localhost'))

    def test_save(self):
        # ensure uuid is filled on save
        widget_host = models.WidgetHost(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        widget_host.save()
        self.assertIn(len(widget_host.uuid), [21, 22])

    def test_get_absolute_url(self):
        widget_host = models.WidgetHost(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        widget_host.save()
        self.assertEqual(widget_host.get_absolute_url(), '/widget/{}/'.format(widget_host.uuid))
