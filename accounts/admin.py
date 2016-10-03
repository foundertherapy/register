
import django.contrib.admin
import accountsplus.admin

from . import models


@django.contrib.admin.register(models.User)
class UserAdmin(accountsplus.admin.BaseUserAdmin):
    pass


@django.contrib.admin.register(models.Company)
class CompanyAdmin(accountsplus.admin.BaseCompanyAdmin):
    pass
