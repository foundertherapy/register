from __future__ import unicode_literals

import unittest

from django.test import TestCase
import django.db

from .. import models


class CobrandCompanyTestCase(TestCase):
    def test_unique(self):
        # ensure company_name and slug are unique
        cobrand_company = models.CobrandCompany.objects.create(
            company_name='test', contact_email='a@a.com', contact_name='test user')
        self.assertRaises(
            django.db.IntegrityError,
            lambda: models.CobrandCompany.objects.create(company_name='test', contact_email='a@a.com', contact_name='test user'))

    def test_save(self):
        # ensure slug and uuid are filled on save
        cobrand_company = models.CobrandCompany(company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        cobrand_company.save()
        self.assertEqual(cobrand_company.slug, 'test-company-ltd')
        self.assertEqual(len(cobrand_company.uuid), 22)

    def test_get_absolute_url(self):
        cobrand_company = models.CobrandCompany(company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        cobrand_company.save()
        self.assertEqual(cobrand_company.get_absolute_url(), '/brand/{}/'.format(cobrand_company.uuid))

    def test_get_redirect_url(self):
        cobrand_company = models.CobrandCompany(company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        cobrand_company.save()
        self.assertEqual(cobrand_company.get_redirect_url(), '/brand/r/{}/'.format(cobrand_company.slug))

    def test_get_logo_filename(self):
        cobrand_company = models.CobrandCompany(company_name='Test. Company, Ltd', contact_email='a@a.com', contact_name='test user')
        cobrand_company.save()
        self.assertEqual(cobrand_company.get_logo_filename(), '{}.png'.format(cobrand_company.uuid))
