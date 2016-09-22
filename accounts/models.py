from __future__ import unicode_literals

import django.db.models
import accountsplus.models


class Company(accountsplus.models.BaseCompany):
    pass


class User(accountsplus.models.BaseUser):
    company = django.db.models.ForeignKey(Company, null=True, related_name='%(app_label)s_%(class)s_users')

