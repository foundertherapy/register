# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import shortuuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20151026_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='widgetsubmission',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 17, 20, 29, 222646), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='widgetsubmission',
            name='updated_on',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 29, 17, 20, 29, 222677), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='widgetsubmission',
            name='company_source',
            field=shortuuidfield.fields.ShortUUIDField(db_index=True, max_length=22, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
