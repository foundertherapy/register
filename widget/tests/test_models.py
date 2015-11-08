from __future__ import unicode_literals

import django.db

from django.test import TestCase

from widget import models


class WidgetSubmissionTestCase(TestCase):
    def test_unique(self):
        # ensure company_name is unique
        models.WidgetSubmission.objects.create(company_name='test', contact_email='a@a.com', contact_name='test user')
        self.assertRaises(
            django.db.IntegrityError,
            lambda: models.WidgetSubmission.objects.create(company_name='test', contact_email='a@a.com', contact_name='test user'))

    def test_save(self):
        # ensure uunid is filled on save
        widget_submission = models.WidgetSubmission(
            company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        widget_submission.save()
        self.assertEqual(len(widget_submission.uuid), 22)

    def test_get_absolute_url(self):
        widget_submission = models.WidgetSubmission(
            company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        widget_submission.save()
        self.assertEqual(widget_submission.get_absolute_url(), '/widget/{}/'.format(widget_submission.uuid))
