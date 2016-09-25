from __future__ import unicode_literals

import django.test


class URLsTestCase(django.test.TestCase):
    fixtures = ('test_users.json', 'test_companies.json', 'test_groups.json', )

    def setUp(self):
        self.client = django.test.Client()

    def test_login_redirect(self):
        r = self.client.get('/login/', follow=False)
        self.assertEqual(r.status_code, 302)

    def test_users_admin_page(self):
        c = django.test.client.Client()
        self.assertTrue(c.login(email='superuser@example.com', password='password'))
        r = c.get('/admin/accounts/user/')
        self.assertEqual(r.status_code, 200)
