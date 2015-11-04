# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cobrandingregistration',
            name='company_logo',
        ),
        migrations.AlterField(
            model_name='cobrandingregistration',
            name='cobrand_id',
            field=shortuuidfield.fields.ShortUUIDField(db_index=True, max_length=22, null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
