# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_cobrandingregistration_company_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cobrandingregistration',
            name='co_branding_id',
            field=models.CharField(max_length=100, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cobrandingregistration',
            name='company_name',
            field=models.CharField(max_length=30),
            preserve_default=True,
        ),
    ]
