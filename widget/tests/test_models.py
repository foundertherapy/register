from __future__ import unicode_literals

import django.db

from django.test import TestCase

from widget import models


class WidgetSubmissionTestCase(TestCase):
    def test_unique(self):
        # ensure company_name is unique
        models.WidgetHost.objects.create(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        self.assertRaises(
            django.db.IntegrityError,
            lambda: models.WidgetHost.objects.create(contact_email='a@a.com', contact_name='test user', host_url='http://localhost'))

    def test_save(self):
        # ensure uuid is filled on save
        widget_submission = models.WidgetHost(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        widget_submission.save()
        self.assertEqual(len(widget_submission.uuid), 22)

    def test_get_absolute_url(self):
        widget_submission = models.WidgetHost(contact_email='a@a.com', contact_name='test user', host_url='http://localhost')
        widget_submission.save()
        self.assertEqual(widget_submission.get_absolute_url(), '/widget/{}/'.format(widget_submission.uuid))
